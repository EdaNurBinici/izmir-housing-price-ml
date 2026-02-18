"""
Configuration file loading module
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
        Initializes the config loader

        Args:
            config_path: Path to config file
        """
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Loads the config file"""
        try:
            config_file = Path(self.config_path)
            if not config_file.exists():
                # Try from project root
                config_file = Path(__file__).parent.parent / self.config_path
                if not config_file.exists():
                    raise FileNotFoundError(f"Config file not found: {self.config_path}")

            with open(config_file, encoding="utf-8") as f:
                self.config = yaml.safe_load(f)

            logger.info(f"Configuration loaded successfully: {self.config_path}")
        except Exception as e:
            logger.error(f"Configuration loading error: {e}")
            raise

    def get(self, key: str, default: Any = None) -> Any:
        """
        Gets config value (dot notation for nested keys)

        Args:
            key: Config key (e.g., "model.max_iter")
            default: Default value

        Returns:
            Config value
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
        """Gets data file path"""
        return self.get(f"data.{key}", "")

    def get_model_config(self) -> Dict[str, Any]:
        """Returns model configuration"""
        return self.get("model", {})

    def get_cleaning_config(self) -> Dict[str, Any]:
        """Returns data cleaning configuration"""
        return self.get("data_cleaning", {})
