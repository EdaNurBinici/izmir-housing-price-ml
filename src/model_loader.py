"""
Model loading and management module
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import joblib
import pandas as pd

from .config_loader import ConfigLoader
from .exceptions import DataLoadError, ModelLoadError

logger = logging.getLogger(__name__)


class ModelLoader:
    """Model and data file loading class"""

    def __init__(self, config: ConfigLoader):
        """
        Initializes the model loader

        Args:
            config: ConfigLoader instance
        """
        self.config = config
        self.model = None
        self.ilce_listesi: List[str] = []
        self.ev_tipleri: List[str] = []
        self.metrikler: Dict[str, Any] = {}
        self.onem_duzeyleri: pd.DataFrame = pd.DataFrame()
        self.ilce_skorlari: Dict[str, float] = {}
        self.raw_df: Optional[pd.DataFrame] = None

    def load_all(self) -> bool:
        """
        Loads all model and data files

        Returns:
            True if loading successful

        Raises:
            ModelLoadError: Model loading error
            DataLoadError: Data loading error
        """
        try:
            logger.info("Loading model and data files...")

            # Model load
            model_path = self.config.get_data_path("model_path")
            self.model = self._load_model(model_path)

            # District list
            ilceler_path = self.config.get_data_path("ilceler_path")
            self.ilce_listesi = self._load_pickle(ilceler_path)

            # Property types
            tipler_path = self.config.get_data_path("tipler_path")
            self.ev_tipleri = self._load_pickle(tipler_path)

            # Metrics
            metrikler_path = self.config.get_data_path("metrikler_path")
            self.metrikler = self._load_pickle(metrikler_path)

            # Feature importance
            onem_path = self.config.get_data_path("onem_duzeyleri_path")
            self.onem_duzeyleri = self._load_pickle(onem_path)

            # District scores
            ilce_skor_path = self.config.get_data_path("ilce_skorlari_path")
            ilce_skor_data = self._load_pickle(ilce_skor_path)
            # Convert Series to dict if needed
            if hasattr(ilce_skor_data, "to_dict"):
                self.ilce_skorlari = ilce_skor_data.to_dict()
            elif isinstance(ilce_skor_data, dict):
                self.ilce_skorlari = ilce_skor_data
            else:
                self.ilce_skorlari = {}

            # Raw data
            raw_data_path = self.config.get_data_path("raw_data")
            self.raw_df = self._load_dataframe(raw_data_path)

            logger.info("All files loaded successfully")
            return True

        except Exception as e:
            logger.error(f"File loading error: {e}")
            raise

    def _load_model(self, path: str):
        """Loads model file"""
        try:
            file_path = Path(path)
            if not file_path.exists():
                # Try from project root
                file_path = Path(__file__).parent.parent / path
                if not file_path.exists():
                    raise FileNotFoundError(f"Model file not found: {path}")

            logger.info(f"Loading model: {file_path}")
            return joblib.load(file_path)
        except Exception as e:
            logger.error(f"Model loading error: {e}")
            raise ModelLoadError(f"Model could not be loaded: {e}")

    def _load_pickle(self, path: str):
        """Loads pickle file"""
        try:
            file_path = Path(path)
            if not file_path.exists():
                file_path = Path(__file__).parent.parent / path
                if not file_path.exists():
                    raise FileNotFoundError(f"File not found: {path}")

            return joblib.load(file_path)
        except Exception as e:
            logger.error(f"Pickle loading error ({path}): {e}")
            raise ModelLoadError(f"File could not be loaded ({path}): {e}")

    def _load_dataframe(self, path: str) -> pd.DataFrame:
        """Loads CSV file as DataFrame"""
        try:
            file_path = Path(path)
            if not file_path.exists():
                file_path = Path(__file__).parent.parent / path
                if not file_path.exists():
                    raise FileNotFoundError(f"Data file not found: {path}")

            logger.info(f"Loading data: {file_path}")
            return pd.read_csv(file_path)
        except Exception as e:
            logger.error(f"Data loading error: {e}")
            raise DataLoadError(f"Data could not be loaded: {e}")

    def is_loaded(self) -> bool:
        """Checks if all files are loaded"""
        return (
            self.model is not None
            and len(self.ilce_listesi) > 0
            and len(self.ev_tipleri) > 0
            and len(self.metrikler) > 0
            and self.raw_df is not None
        )

    def get_ilce_skoru(self, ilce: str, default: float = 50000.0) -> float:
        """
        Returns district score

        Args:
            ilce: District name
            default: Default score

        Returns:
            District score
        """
        return self.ilce_skorlari.get(ilce, default)
