"""
Luxury score calculation module
"""

import logging
from typing import Any, Dict

from .config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class LuxuryScoreCalculator:
    """Luxury score calculator class"""

    def __init__(self, config: ConfigLoader):
        """
        Initializes the luxury score calculator

        Args:
            config: ConfigLoader instance
        """
        self.config = config
        self.luxury_config = config.get("luxury_score", {})
        self._load_config()

    def _load_config(self) -> None:
        """Loads parameters from config"""
        self.price_thresholds = self.luxury_config.get("price_thresholds", {})
        self.area_thresholds = self.luxury_config.get("area_thresholds", {})
        self.luxury_districts = self.luxury_config.get("luxury_districts", [])
        self.luxury_types = self.luxury_config.get("luxury_types", [])
        self.age_weights = self.luxury_config.get("age_weights", {})

    def calculate(self, fiyat: float, m2: float, ilce: str, tip: str, yas: int) -> Dict[str, Any]:
        """
        Calculates the luxury score

        Args:
            fiyat: Property price
            m2: Area in square meters
            ilce: District name
            tip: Property type
            yas: Building age

        Returns:
            Dict containing score and details
        """
        puan = 0
        detaylar = {}

        # Price score
        fiyat_puan = self._calculate_price_score(fiyat)
        puan += fiyat_puan
        detaylar["price_score"] = fiyat_puan

        # Area score
        m2_puan = self._calculate_area_score(m2)
        puan += m2_puan
        detaylar["area_score"] = m2_puan

        # District score
        ilce_puan = self._calculate_district_score(ilce)
        puan += ilce_puan
        detaylar["district_score"] = ilce_puan

        # Property type score
        tip_puan = self._calculate_type_score(tip)
        puan += tip_puan
        detaylar["property_type_score"] = tip_puan

        # Age score
        yas_puan = self._calculate_age_score(yas)
        puan += yas_puan
        detaylar["building_age_score"] = yas_puan

        # Limit score to 0-100 range
        final_skor = min(100, max(0, puan))

        # Determine category (English)
        kategori = self._get_category(final_skor)

        return {"skor": final_skor, "kategori": kategori, "detaylar": detaylar}

    def _calculate_price_score(self, fiyat: float) -> int:
        """Calculates price score"""
        ultra = self.price_thresholds.get("ultra_luxury", 20000000)
        luxury = self.price_thresholds.get("luxury", 10000000)
        premium = self.price_thresholds.get("premium", 5000000)

        if fiyat > ultra:
            return 40
        elif fiyat > luxury:
            return 30
        elif fiyat > premium:
            return 20
        else:
            return 5

    def _calculate_area_score(self, m2: float) -> int:
        """Calculates area score"""
        very_large = self.area_thresholds.get("very_large", 350)
        large = self.area_thresholds.get("large", 200)
        medium = self.area_thresholds.get("medium", 130)

        if m2 > very_large:
            return 25
        elif m2 > large:
            return 15
        elif m2 > medium:
            return 10
        else:
            return 0

    def _calculate_district_score(self, ilce: str) -> int:
        """Calculates district score"""
        if ilce in self.luxury_districts:
            return 20
        return 0

    def _calculate_type_score(self, tip: str) -> int:
        """Calculates property type score"""
        if tip in self.luxury_types:
            return 15
        return 0

    def _calculate_age_score(self, yas: int) -> int:
        """Calculates building age score"""
        if yas == 0:
            return self.age_weights.get("new", 15)
        elif yas <= 3:
            return self.age_weights.get("very_recent", 10)
        elif yas <= 8:
            return self.age_weights.get("recent", 5)
        elif yas <= 15:
            return self.age_weights.get("moderate", 0)
        elif yas <= 25:
            return self.age_weights.get("old", -5)
        elif yas <= 40:
            return self.age_weights.get("very_old", -10)
        else:
            return self.age_weights.get("ancient", -15)

    def _get_category(self, skor: float) -> str:
        """Returns category based on score"""
        if skor >= 85:
            return "Ultra Luxury ⭐"
        elif skor >= 65:
            return "Luxury Property ✨"
        elif skor >= 45:
            return "Comfortable 🏠"
        else:
            return "Standard"
