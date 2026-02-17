"""
Logging sistemi kurulum modülü
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


def setup_logging(
    log_level: str = "INFO",
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    log_file: Optional[str] = None,
    max_bytes: int = 10485760,
    backup_count: int = 5,
) -> None:
    """
    Logging sistemini yapılandırır

    Args:
        log_level: Log seviyesi (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log formatı
        log_file: Log dosyası yolu (None ise sadece console)
        max_bytes: Log dosyası maksimum boyutu
        backup_count: Yedek log dosyası sayısı
    """
    # Log seviyesini ayarla
    level = getattr(logging, log_level.upper(), logging.INFO)

    # Root logger'ı yapılandır
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Mevcut handler'ları temizle
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(log_format)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File handler (eğer belirtilmişse)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    logging.info("Logging sistemi başlatıldı")


def get_logger(name: str) -> logging.Logger:
    """
    Belirtilen isimle logger döndürür

    Args:
        name: Logger adı

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
