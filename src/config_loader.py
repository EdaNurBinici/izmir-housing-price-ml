"""
Yapılandırma dosyası yükleme modülü
"""

import logging
from pathlib import Path
from typing import Any, Dict

import yaml

logger = logging.getLogger(__name__)


class ConfigLoader:
    """YAML config dosyasını yükleyen ve yöneten sınıf"""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Config loader'ı başlatır

        Args:
            config_path: Config dosyasının yolu
        """
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Config dosyasını yükler"""
        try:
            config_file = Path(self.config_path)
            if not config_file.exists():
                # Proje root'undan dene
                config_file = Path(__file__).parent.parent / self.config_path
                if not config_file.exists():
                    raise FileNotFoundError(f"Config dosyası bulunamadı: {self.config_path}")

            with open(config_file, encoding="utf-8") as f:
                self.config = yaml.safe_load(f)

            logger.info(f"Config dosyası başarıyla yüklendi: {self.config_path}")
        except Exception as e:
            logger.error(f"Config yükleme hatası: {e}")
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """
        Config değerini alır (nested key'ler için nokta notasyonu)

        Args:
            key: Config anahtarı (örn: "model.max_iter")
            default: Varsayılan değer

        Returns:
            Config değeri
        """
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def get_data_path(self, key: str) -> str:
        """Data dosya yolu alır"""
        return self.get(f"data.{key}", "")

    def get_model_config(self) -> Dict[str, Any]:
        """Model yapılandırmasını döndürür"""
        return self.get("model", {})

    def get_cleaning_config(self) -> Dict[str, Any]:
        """Veri temizleme yapılandırmasını döndürür"""
        return self.get("data_cleaning", {})
