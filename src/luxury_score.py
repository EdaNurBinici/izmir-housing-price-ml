"""
Lüks skoru hesaplama modülü
"""

import logging
from typing import Any, Dict

from .config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class LuxuryScoreCalculator:
    """Lüks skoru hesaplayan sınıf"""

    def __init__(self, config: ConfigLoader):
        """
        Luxury score calculator'ı başlatır

        Args:
            config: ConfigLoader instance
        """
        self.config = config
        self.luxury_config = config.get("luxury_score", {})
        self._load_config()

    def _load_config(self) -> None:
        """Config'den parametreleri yükler"""
        self.price_thresholds = self.luxury_config.get("price_thresholds", {})
        self.area_thresholds = self.luxury_config.get("area_thresholds", {})
        self.luxury_districts = self.luxury_config.get("luxury_districts", [])
        self.luxury_types = self.luxury_config.get("luxury_types", [])
        self.age_weights = self.luxury_config.get("age_weights", {})

    def calculate(self, fiyat: float, m2: float, ilce: str, tip: str, yas: int) -> Dict[str, Any]:
        """
        Lüks skorunu hesaplar

        Args:
            fiyat: Konut fiyatı
            m2: Metrekare
            ilce: İlçe adı
            tip: Ev tipi
            yas: Bina yaşı

        Returns:
            Skor ve detaylar içeren dict
        """
        puan = 0
        detaylar = {}

        # Fiyat puanı
        fiyat_puan = self._calculate_price_score(fiyat)
        puan += fiyat_puan
        detaylar["fiyat_puan"] = fiyat_puan

        # Metrekare puanı
        m2_puan = self._calculate_area_score(m2)
        puan += m2_puan
        detaylar["m2_puan"] = m2_puan

        # İlçe puanı
        ilce_puan = self._calculate_district_score(ilce)
        puan += ilce_puan
        detaylar["ilce_puan"] = ilce_puan

        # Ev tipi puanı
        tip_puan = self._calculate_type_score(tip)
        puan += tip_puan
        detaylar["tip_puan"] = tip_puan

        # Yaş puanı
        yas_puan = self._calculate_age_score(yas)
        puan += yas_puan
        detaylar["yas_puan"] = yas_puan

        # Skoru 0-100 aralığına sınırla
        final_skor = min(100, max(0, puan))

        # Kategori belirle
        kategori = self._get_category(final_skor)

        return {"skor": final_skor, "kategori": kategori, "detaylar": detaylar}

    def _calculate_price_score(self, fiyat: float) -> int:
        """Fiyat puanını hesaplar"""
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
        """Metrekare puanını hesaplar"""
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
        """İlçe puanını hesaplar"""
        if ilce in self.luxury_districts:
            return 20
        return 0

    def _calculate_type_score(self, tip: str) -> int:
        """Ev tipi puanını hesaplar"""
        if tip in self.luxury_types:
            return 15
        return 0

    def _calculate_age_score(self, yas: int) -> int:
        """Bina yaşı puanını hesaplar"""
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
        """Skora göre kategori döndürür"""
        if skor >= 85:
            return "Ultra Lüks ⭐"
        elif skor >= 65:
            return "Lüks Konut ✨"
        elif skor >= 45:
            return "Konforlu 🏠"
        else:
            return "Standart"
