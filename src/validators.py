"""
Veri doğrulama modülü
"""

import logging
from typing import Any, Dict, Optional

import pandas as pd

from .exceptions import ValidationError

logger = logging.getLogger(__name__)


class InputValidator:
    """Kullanıcı girdilerini doğrulayan sınıf"""

    def __init__(
        self,
        price_min: int = 100000,
        price_max: int = 50000000,
        area_min: int = 20,
        area_max: int = 1000,
        age_min: int = 0,
        age_max: int = 100,
        room_min: int = 1,
        room_max: int = 10,
        salon_min: int = 1,
        salon_max: int = 5,
    ):
        """
        Validator'ı başlatır

        Args:
            price_min: Minimum fiyat
            price_max: Maksimum fiyat
            area_min: Minimum metrekare
            area_max: Maksimum metrekare
            age_min: Minimum bina yaşı
            age_max: Maksimum bina yaşı
            room_min: Minimum oda sayısı
            room_max: Maksimum oda sayısı
            salon_min: Minimum salon sayısı
            salon_max: Maksimum salon sayısı
        """
        self.price_min = price_min
        self.price_max = price_max
        self.area_min = area_min
        self.area_max = area_max
        self.age_min = age_min
        self.age_max = age_max
        self.room_min = room_min
        self.room_max = room_max
        self.salon_min = salon_min
        self.salon_max = salon_max

    def validate_input(
        self,
        ilce: str,
        ev_tipi: str,
        m2: float,
        oda: int,
        salon: int,
        yas: int,
        valid_ilceler: Optional[list] = None,
        valid_tipler: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Kullanıcı girdilerini doğrular

        Args:
            ilce: İlçe adı
            ev_tipi: Ev tipi
            m2: Metrekare
            oda: Oda sayısı
            salon: Salon sayısı
            yas: Bina yaşı
            valid_ilceler: Geçerli ilçe listesi
            valid_tipler: Geçerli ev tipi listesi

        Returns:
            Doğrulanmış veriler

        Raises:
            ValidationError: Doğrulama hatası durumunda
        """
        errors = []

        # İlçe kontrolü
        if not ilce or not isinstance(ilce, str):
            errors.append("İlçe boş olamaz")
        elif valid_ilceler and ilce not in valid_ilceler:
            errors.append(f"Geçersiz ilçe: {ilce}")

        # Ev tipi kontrolü
        if not ev_tipi or not isinstance(ev_tipi, str):
            errors.append("Ev tipi boş olamaz")
        elif valid_tipler and ev_tipi not in valid_tipler:
            errors.append(f"Geçersiz ev tipi: {ev_tipi}")

        # Metrekare kontrolü
        if not isinstance(m2, (int, float)) or m2 < self.area_min or m2 > self.area_max:
            errors.append(f"Metrekare {self.area_min}-{self.area_max} arasında olmalıdır")

        # Oda sayısı kontrolü
        if not isinstance(oda, int) or oda < self.room_min or oda > self.room_max:
            errors.append(f"Oda sayısı {self.room_min}-{self.room_max} arasında olmalıdır")

        # Salon sayısı kontrolü
        if not isinstance(salon, int) or salon < self.salon_min or salon > self.salon_max:
            errors.append(f"Salon sayısı {self.salon_min}-{self.salon_max} arasında olmalıdır")

        # Bina yaşı kontrolü
        if not isinstance(yas, int) or yas < self.age_min or yas > self.age_max:
            errors.append(f"Bina yaşı {self.age_min}-{self.age_max} arasında olmalıdır")

        if errors:
            error_msg = "; ".join(errors)
            logger.warning(f"Doğrulama hatası: {error_msg}")
            raise ValidationError(error_msg)

        return {
            "ilce": ilce,
            "ev_tipi": ev_tipi,
            "m2": float(m2),
            "oda": int(oda),
            "salon": int(salon),
            "yas": int(yas),
        }

    def validate_dataframe(self, df: pd.DataFrame, required_columns: list) -> None:
        """
        DataFrame'i doğrular

        Args:
            df: Doğrulanacak DataFrame
            required_columns: Gerekli sütunlar

        Raises:
            ValidationError: Doğrulama hatası durumunda
        """
        if df.empty:
            raise ValidationError("DataFrame boş")

        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValidationError(f"Eksik sütunlar: {missing_columns}")
