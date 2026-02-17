"""
Model Eğitim Scripti - Senior Seviyesinde Refactor Edilmiş Versiyon
Bu dosya, src/train_model.py modülünü kullanarak model eğitimini başlatır.
"""

import sys
from pathlib import Path

# src klasörünü path'e ekle
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from src.train_model import main

if __name__ == "__main__":
    main()
