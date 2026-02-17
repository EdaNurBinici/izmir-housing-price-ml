"""
Fiyat tahmin modülü
"""
import pandas as pd
from typing import Dict, Any
import logging

from .exceptions import PredictionError
from .model_loader import ModelLoader
from .luxury_score import LuxuryScoreCalculator
from .validators import InputValidator

logger = logging.getLogger(__name__)


class PricePredictor:
    """Fiyat tahmini yapan sınıf"""
    
    def __init__(
        self,
        model_loader: ModelLoader,
        luxury_calculator: LuxuryScoreCalculator,
        validator: InputValidator
    ):
        """
        Predictor'ı başlatır
        
        Args:
            model_loader: ModelLoader instance
            luxury_calculator: LuxuryScoreCalculator instance
            validator: InputValidator instance
        """
        self.model_loader = model_loader
        self.luxury_calculator = luxury_calculator
        self.validator = validator
    
    def predict(
        self,
        ilce: str,
        ev_tipi: str,
        m2: float,
        oda: int,
        salon: int,
        yas: int
    ) -> Dict[str, Any]:
        """
        Fiyat tahmini yapar ve lüks skorunu hesaplar
        
        Args:
            ilce: İlçe adı
            ev_tipi: Ev tipi
            m2: Metrekare
            oda: Oda sayısı
            salon: Salon sayısı
            yas: Bina yaşı
            
        Returns:
            Tahmin sonuçları içeren dict
            
        Raises:
            PredictionError: Tahmin hatası
        """
        try:
            # Girdileri doğrula
            validated = self.validator.validate_input(
                ilce=ilce,
                ev_tipi=ev_tipi,
                m2=m2,
                oda=oda,
                salon=salon,
                yas=yas,
                valid_ilceler=self.model_loader.ilce_listesi,
                valid_tipler=self.model_loader.ev_tipleri
            )
            
            # İlçe skorunu al
            ilce_skoru = self.model_loader.get_ilce_skoru(ilce)
            
            # Model için input hazırla
            input_data = pd.DataFrame({
                'area': [validated['m2']],
                'age': [validated['yas']],
                'district': [validated['ilce']],
                'left': [validated['ev_tipi']],
                'toplam_oda': [validated['oda'] + validated['salon']],
                'ilce_skoru': [ilce_skoru]
            })
            
            # Tahmin yap
            logger.info(f"Tahmin yapılıyor: {validated}")
            tahmin = self.model_loader.model.predict(input_data)[0]
            fiyat = int(tahmin)
            
            # Lüks skorunu hesapla
            luxury_result = self.luxury_calculator.calculate(
                fiyat=fiyat,
                m2=validated['m2'],
                ilce=validated['ilce'],
                tip=validated['ev_tipi'],
                yas=validated['yas']
            )
            
            return {
                'tahmini_fiyat': fiyat,
                'luxury_score': luxury_result['skor'],
                'luxury_category': luxury_result['kategori'],
                'luxury_details': luxury_result['detaylar'],
                'input': validated
            }
            
        except Exception as e:
            logger.error(f"Tahmin hatası: {e}")
            raise PredictionError(f"Tahmin yapılamadı: {e}")
