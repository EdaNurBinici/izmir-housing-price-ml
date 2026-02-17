"""
Luxury score calculator testleri
"""

import sys
from pathlib import Path

# src klasörünü path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from src.config_loader import ConfigLoader
from src.luxury_score import LuxuryScoreCalculator


class TestLuxuryScoreCalculator:
    """LuxuryScoreCalculator test sınıfı"""

    def setup_method(self):
        """Her test öncesi çalışır"""
        config = ConfigLoader("config/config.yaml")
        self.calculator = LuxuryScoreCalculator(config)

    def test_ultra_luxury(self):
        """Ultra lüks konut testi"""
        result = self.calculator.calculate(fiyat=25000000, m2=400, ilce="Çeşme", tip="Villa", yas=0)
        assert result["skor"] >= 85
        assert result["kategori"] == "Ultra Luxury ⭐"

    def test_standard_property(self):
        """Standart konut testi"""
        result = self.calculator.calculate(fiyat=2000000, m2=100, ilce="Buca", tip="Daire", yas=20)
        assert result["skor"] < 45
        assert result["kategori"] == "Standard"

    def test_score_range(self):
        """Skor aralığı testi"""
        result = self.calculator.calculate(
            fiyat=5000000, m2=150, ilce="Urla", tip="Müstakil", yas=5
        )
        assert 0 <= result["skor"] <= 100


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
