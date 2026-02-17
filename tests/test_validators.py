"""
Validator testleri
"""
import pytest
import sys
from pathlib import Path

# src klasörünü path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from src.validators import InputValidator
from src.exceptions import ValidationError


class TestInputValidator:
    """InputValidator test sınıfı"""
    
    def setup_method(self):
        """Her test öncesi çalışır"""
        self.validator = InputValidator()
    
    def test_valid_input(self):
        """Geçerli girdi testi"""
        result = self.validator.validate_input(
            ilce="Çeşme",
            ev_tipi="Villa",
            m2=150.0,
            oda=3,
            salon=1,
            yas=5
        )
        assert result['ilce'] == "Çeşme"
        assert result['m2'] == 150.0
    
    def test_invalid_area(self):
        """Geçersiz metrekare testi"""
        with pytest.raises(ValidationError):
            self.validator.validate_input(
                ilce="Çeşme",
                ev_tipi="Villa",
                m2=10,  # Çok küçük
                oda=3,
                salon=1,
                yas=5
            )
    
    def test_invalid_age(self):
        """Geçersiz yaş testi"""
        with pytest.raises(ValidationError):
            self.validator.validate_input(
                ilce="Çeşme",
                ev_tipi="Villa",
                m2=150,
                oda=3,
                salon=1,
                yas=150  # Çok büyük
            )
    
    def test_empty_district(self):
        """Boş ilçe testi"""
        with pytest.raises(ValidationError):
            self.validator.validate_input(
                ilce="",
                ev_tipi="Villa",
                m2=150,
                oda=3,
                salon=1,
                yas=5
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
