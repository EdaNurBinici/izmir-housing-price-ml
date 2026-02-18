"""
Price prediction module
"""

import logging
from typing import Any, Dict

import pandas as pd

from .exceptions import PredictionError
from .luxury_score import LuxuryScoreCalculator
from .model_loader import ModelLoader
from .validators import InputValidator

logger = logging.getLogger(__name__)


class PricePredictor:
    """Price prediction class"""

    def __init__(
        self,
        model_loader: ModelLoader,
        luxury_calculator: LuxuryScoreCalculator,
        validator: InputValidator,
    ):
        """
        Initializes the predictor

        Args:
            model_loader: ModelLoader instance
            luxury_calculator: LuxuryScoreCalculator instance
            validator: InputValidator instance
        """
        self.model_loader = model_loader
        self.luxury_calculator = luxury_calculator
        self.validator = validator

    def predict(
        self, ilce: str, ev_tipi: str, m2: float, oda: int, salon: int, yas: int
    ) -> Dict[str, Any]:
        """
        Makes price prediction and calculates luxury score

        Args:
            ilce: District name
            ev_tipi: Property type
            m2: Area in square meters
            oda: Number of rooms
            salon: Number of living rooms
            yas: Building age

        Returns:
            Dict containing prediction results

        Raises:
            PredictionError: Prediction error
        """
        try:
            # Validate inputs
            validated = self.validator.validate_input(
                ilce=ilce,
                ev_tipi=ev_tipi,
                m2=m2,
                oda=oda,
                salon=salon,
                yas=yas,
                valid_ilceler=self.model_loader.ilce_listesi,
                valid_tipler=self.model_loader.ev_tipleri,
            )

            # Get district score
            ilce_skoru = self.model_loader.get_ilce_skoru(ilce)

            # Prepare input for model
            input_data = pd.DataFrame(
                {
                    "area": [validated["m2"]],
                    "age": [validated["yas"]],
                    "district": [validated["ilce"]],
                    "left": [validated["ev_tipi"]],
                    "toplam_oda": [validated["oda"] + validated["salon"]],
                    "ilce_skoru": [ilce_skoru],
                }
            )

            # Make prediction
            logger.info(f"Making prediction: {validated}")
            tahmin = self.model_loader.model.predict(input_data)[0]
            fiyat = int(tahmin)

            # Calculate luxury score
            luxury_result = self.luxury_calculator.calculate(
                fiyat=fiyat,
                m2=validated["m2"],
                ilce=validated["ilce"],
                tip=validated["ev_tipi"],
                yas=validated["yas"],
            )

            return {
                "tahmini_fiyat": fiyat,
                "luxury_score": luxury_result["skor"],
                "luxury_category": luxury_result["kategori"],
                "luxury_details": luxury_result["detaylar"],
                "input": validated,
            }

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise PredictionError(f"Prediction failed: {e}")
