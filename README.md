# 🏠 Izmir Housing Price Prediction System

[![CI](https://github.com/EdaNurBinici/izmir-housing-price-ml/actions/workflows/ci.yml/badge.svg)](https://github.com/EdaNurBinici/izmir-housing-price-ml/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A machine learning-based system for predicting housing prices in Izmir, Turkey, with an integrated luxury scoring algorithm.

> Originally developed for the "Introduction to Artificial Intelligence" course.

**Quick Overview:** ML-powered housing price predictor with 87%+ accuracy, custom luxury scoring algorithm, interactive Streamlit UI. Production-inspired architecture: modular structure, logging, and error handling.

## ✨ Features

- 🎯 **Modular Architecture:** Professional-grade code organization
- 📊 **Advanced Data Analysis:** Comprehensive EDA and visualization tools
- 🤖 **Machine Learning:** High-performance HistGradientBoostingRegressor
- 💎 **Luxury Score:** Custom-built feature engineering algorithm for property valuation
- 🎨 **Modern UI:** Interactive web interface built with Streamlit
- 📝 **Logging System:** Professional logging infrastructure
- ⚙️ **Configuration Management:** YAML-based configuration
- ✅ **Testing Support:** Unit tests for code quality assurance

## 💎 How the Luxury Score Works

The custom-built algorithm evaluates properties beyond just price per square meter. It factors in the district's prestige, building age, and room-to-area ratio to categorize properties from standard to ultra-luxury tiers.

## 📸 Application Screenshots

![Live Prediction App](docs/images/Live-Prediction-App.png?v=2)
*Interactive Streamlit interface for real-time housing price predictions*

## 👤 Developer

**Eda Nur Binici**

## 🛠️ Technology Stack

- **Python 3.8+**
- **Scikit-learn:** Machine learning (Gradient Boosting)
- **Pandas & NumPy:** Data processing
- **Matplotlib & Seaborn:** Visualization
- **Streamlit:** Web interface
- **PyYAML:** Configuration management
- **Joblib:** Model serialization

## 📋 Requirements

- Python 3.8 or higher
- All dependencies are listed in `requirements.txt`

## 🚀 Quick Start

### Ready to Use - No Training Required! 🎉

The repository includes pre-trained model files (~2MB) and cleaned dataset (~300KB), so you can run the application immediately after cloning.

### Option 1: Automated Setup (Recommended)

**Windows (PowerShell):**
```powershell
.\scripts\setup.ps1
streamlit run app.py
```

**Linux/Mac:**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
streamlit run app.py
```

### Option 2: Manual Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/EdaNurBinici/izmir-housing-price-ml.git
cd izmir-housing-price-ml
```

#### 2. Create Virtual Environment

**Windows (PowerShell):**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Windows (CMD):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

For development (includes linting, formatting, testing tools):
```bash
pip install -r requirements-dev.txt
pre-commit install
```

> **Note:** All dependencies are pinned to exact versions for reproducibility. See [DEPENDENCY_MANAGEMENT.md](DEPENDENCY_MANAGEMENT.md) for update procedures.

#### 4. Launch the Application

```bash
streamlit run app.py
```

The application opens automatically at `http://localhost:8501`

### Optional: Retrain the Model

If you want to retrain the model with your own parameters:

```bash
python model_egitim.py
```

This generates model artifacts in organized directories:

**Models** (`artifacts/models/`):
- `izmir_model.pkl` - Trained HistGradientBoostingRegressor (~1.6MB)

**Encoders** (`artifacts/encoders/`):
- `izmir_ilceler.pkl` - District encodings
- `ev_tipleri.pkl` - Property type encodings
- `ilce_skorlari.pkl` - District target encodings

**Metrics** (`artifacts/metrics/`):
- `model_metrikleri.pkl` - Performance metrics (R², MAE, RMSE)
- `model_onem_duzeyleri.pkl` - Feature importance scores

**Data** (`data/processed/`):
- `data_cleaned.csv` - Cleaned dataset ready for training (~300KB)

> **Note:** Pre-trained models are included in the repository for immediate use. Retraining is optional.

## 🛠️ Development Commands

Using Make (Linux/Mac/Windows with Make installed):
```bash
make help          # Show all available commands
make install       # Install production dependencies
make install-dev   # Install development dependencies
make train         # Train the model
make run           # Run Streamlit app
make test          # Run tests
make lint          # Check code quality
make format        # Format code with black + isort
make clean         # Remove generated files
```

Using scripts directly:
```bash
# Windows
.\scripts\train.ps1
.\scripts\run.ps1

# Linux/Mac
./scripts/train.sh
./scripts/run.sh
```

## 📁 Project Structure

```
izmir-housing-price-ml/
├── .github/
│   └── workflows/
│       └── ci.yml                # GitHub Actions CI/CD pipeline
├── src/                          # Source code modules
│   ├── __init__.py
│   ├── config_loader.py          # YAML configuration loader
│   ├── logger_setup.py           # Logging system
│   ├── exceptions.py             # Custom exceptions
│   ├── validators.py             # Data validation
│   ├── model_loader.py           # Model loading and management
│   ├── luxury_score.py           # Luxury score calculation
│   ├── predictor.py              # Price prediction service
│   ├── data_processor.py         # Data processing and cleaning
│   └── train_model.py            # Model training module
├── config/
│   └── config.yaml               # Main configuration file
├── tests/                        # Unit tests
│   ├── __init__.py
│   ├── test_validators.py
│   └── test_luxury_score.py
├── data/                         # Data directory
│   ├── raw/                      # Original data files
│   └── processed/                # Cleaned data files
│       └── data_cleaned.csv      # Main dataset (6000+ records)
├── artifacts/                    # Model artifacts (generated)
│   ├── models/                   # Trained models (*.pkl)
│   ├── encoders/                 # Encoders and transformers (*.pkl)
│   └── metrics/                  # Performance metrics (*.pkl)
├── docs/                         # Documentation
│   ├── images/                   # Report graphics and visualizations
│   └── README.md                 # Documentation guide
├── scripts/                      # Utility scripts
│   ├── setup.ps1                 # Windows setup script
│   ├── setup.sh                  # Linux/Mac setup script
│   ├── train.ps1                 # Windows training script
│   └── run.ps1                   # Windows run script
├── logs/                         # Application logs (auto-generated)
├── app.py                        # Streamlit web application
├── model_egitim.py               # Model training script
├── grafik.py                     # Visualization script
├── requirements.txt              # Pinned production dependencies
├── requirements.in               # Unpinned dependency specifications
├── requirements-dev.txt          # Development dependencies
├── pyproject.toml                # Python project configuration
├── .pre-commit-config.yaml       # Pre-commit hooks configuration
├── .gitattributes                # Git line ending configuration
├── Makefile                      # Development commands
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
├── CONTRIBUTING.md               # Contribution guidelines
└── README.md                     # This file
```

## 🎯 Usage

Refer to the Quick Start section above for detailed setup and running instructions.

## 📊 Model Performance

Current model metrics (HistGradientBoostingRegressor):

| Metric | Value | Description |
|--------|-------|-------------|
| **R² Score** | 0.87+ | Model accuracy (87%+ variance explained) |
| **MAE** | ~150K TL | Mean Absolute Error |
| **RMSE** | ~200K TL | Root Mean Square Error |

Performance metrics are automatically saved to `model_metrikleri.pkl` after training and displayed in the Streamlit application.

### Feature Importance

Top features influencing predictions:
1. Area (m²) - Property size
2. District Score - Location value
3. Property Type - House category
4. Building Age - Construction year
5. Room Count - Total rooms

Detailed feature importance is available in the application's performance section.

## 🔧 Configuration

All configuration settings are in `config/config.yaml`:

- Data file paths
- Model parameters
- Data cleaning thresholds
- Luxury score parameters
- Logging settings

## 📝 Production-Inspired Architecture & Code Quality

This project follows production-inspired practices with modular architecture, comprehensive logging, and error handling:

* **Architecture & Config:** Clean, modular separation of concerns with robust YAML-based configuration management.
* **Quality Assurance:** Comprehensive unit testing (`pytest`) and automated CI/CD pipelines via GitHub Actions.
* **Code Quality & Styling:** Automated formatting (`Black`, `isort`), fast linting (`Ruff`), and enforced `pre-commit` hooks.
* **Type Safety & Docs:** Fully annotated with Python type hints and comprehensive docstrings across all modules.
* **Reliability:** Custom exception handling and structured logging implemented across the entire ML pipeline.
* **Reproducibility:** Strict dependency pinning for consistent environments.

### Running Quality Checks

```bash
# Format code
make format

# Check code quality
make lint

# Run all checks (format + lint + test)
make format && make lint && make test
```

## 🐛 Troubleshooting

### Quick Start Issues

The repository includes all necessary model files and data. If you encounter issues:

1. Ensure you've installed dependencies: `pip install -r requirements.txt`
2. Check that you're in the project root directory
3. Verify Python version is 3.8 or higher

### Model Files Not Found (Rare)

If the application cannot find model files (this shouldn't happen as they're included):

1. Run `python model_egitim.py` to regenerate
2. Check that `artifacts/` directory exists with subdirectories

### Configuration File Error

If you encounter config loading errors:

1. Verify `config/config.yaml` exists
2. Check YAML syntax validity

### Log Files

Log files are stored in the `logs/` directory with automatic rotation:
- Maximum file size: 5MB
- Backup files kept: 3
- Old logs are automatically archived as `app.log.1`, `app.log.2`, `app.log.3`
- This prevents disk space issues and keeps logs manageable

The directory is created automatically if it doesn't exist.

## 📈 Development Notes

### Adding New Features

1. Create the relevant module in `src/`
2. Add necessary settings to `config/config.yaml`
3. Integrate the feature in `app.py`
4. Add test files

### Updating the Model

1. Retrain the model using `src/train_model.py`
2. Review new metrics
3. Adjust parameters in `config/config.yaml` if needed

---

**Version:** 1.0.0  
**Last Updated:** 2026
