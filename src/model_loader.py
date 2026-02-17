"""
Model yükleme ve yönetim modülü
"""
import joblib
import pandas as pd
from pathlib import Path
from typing import Tuple, Dict, Any, Optional, List
import logging

from .exceptions import ModelLoadError, DataLoadError
from .config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class ModelLoader:
    """Model ve veri dosyalarını yükleyen sınıf"""
    
    def __init__(self, config: ConfigLoader):
        """
        Model loader'ı başlatır
        
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
        Tüm model ve veri dosyalarını yükler
        
        Returns:
            Yükleme başarılı ise True
            
        Raises:
            ModelLoadError: Model yükleme hatası
            DataLoadError: Veri yükleme hatası
        """
        try:
            logger.info("Model ve veri dosyaları yükleniyor...")
            
            # Model yükle
            model_path = self.config.get_data_path("model_path")
            self.model = self._load_model(model_path)
            
            # İlçe listesi
            ilceler_path = self.config.get_data_path("ilceler_path")
            self.ilce_listesi = self._load_pickle(ilceler_path)
            
            # Ev tipleri
            tipler_path = self.config.get_data_path("tipler_path")
            self.ev_tipleri = self._load_pickle(tipler_path)
            
            # Metrikler
            metrikler_path = self.config.get_data_path("metrikler_path")
            self.metrikler = self._load_pickle(metrikler_path)
            
            # Önem düzeyleri
            onem_path = self.config.get_data_path("onem_duzeyleri_path")
            self.onem_duzeyleri = self._load_pickle(onem_path)
            
            # İlçe skorları
            ilce_skor_path = self.config.get_data_path("ilce_skorlari_path")
            ilce_skor_data = self._load_pickle(ilce_skor_path)
            # Series ise dict'e çevir
            if hasattr(ilce_skor_data, 'to_dict'):
                self.ilce_skorlari = ilce_skor_data.to_dict()
            elif isinstance(ilce_skor_data, dict):
                self.ilce_skorlari = ilce_skor_data
            else:
                self.ilce_skorlari = {}
            
            # Ham veri
            raw_data_path = self.config.get_data_path("raw_data")
            self.raw_df = self._load_dataframe(raw_data_path)
            
            logger.info("Tüm dosyalar başarıyla yüklendi")
            return True
            
        except Exception as e:
            logger.error(f"Dosya yükleme hatası: {e}")
            raise
    
    def _load_model(self, path: str):
        """Model dosyasını yükler"""
        try:
            file_path = Path(path)
            if not file_path.exists():
                # Proje root'undan dene
                file_path = Path(__file__).parent.parent / path
                if not file_path.exists():
                    raise FileNotFoundError(f"Model dosyası bulunamadı: {path}")
            
            logger.info(f"Model yükleniyor: {file_path}")
            return joblib.load(file_path)
        except Exception as e:
            logger.error(f"Model yükleme hatası: {e}")
            raise ModelLoadError(f"Model yüklenemedi: {e}")
    
    def _load_pickle(self, path: str):
        """Pickle dosyasını yükler"""
        try:
            file_path = Path(path)
            if not file_path.exists():
                file_path = Path(__file__).parent.parent / path
                if not file_path.exists():
                    raise FileNotFoundError(f"Dosya bulunamadı: {path}")
            
            return joblib.load(file_path)
        except Exception as e:
            logger.error(f"Pickle yükleme hatası ({path}): {e}")
            raise ModelLoadError(f"Dosya yüklenemedi ({path}): {e}")
    
    def _load_dataframe(self, path: str) -> pd.DataFrame:
        """CSV dosyasını DataFrame olarak yükler"""
        try:
            file_path = Path(path)
            if not file_path.exists():
                file_path = Path(__file__).parent.parent / path
                if not file_path.exists():
                    raise FileNotFoundError(f"Veri dosyası bulunamadı: {path}")
            
            logger.info(f"Veri yükleniyor: {file_path}")
            return pd.read_csv(file_path)
        except Exception as e:
            logger.error(f"Veri yükleme hatası: {e}")
            raise DataLoadError(f"Veri yüklenemedi: {e}")
    
    def is_loaded(self) -> bool:
        """Tüm dosyaların yüklenip yüklenmediğini kontrol eder"""
        return (
            self.model is not None and
            len(self.ilce_listesi) > 0 and
            len(self.ev_tipleri) > 0 and
            len(self.metrikler) > 0 and
            self.raw_df is not None
        )
    
    def get_ilce_skoru(self, ilce: str, default: float = 50000.0) -> float:
        """
        İlçe skorunu döndürür
        
        Args:
            ilce: İlçe adı
            default: Varsayılan skor
            
        Returns:
            İlçe skoru
        """
        return self.ilce_skorlari.get(ilce, default)
