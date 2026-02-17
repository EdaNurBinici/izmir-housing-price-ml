# 🏠 Izmir Housing Price Prediction System

[![CI](https://github.com/EdaNurBinici/izmir-housing-price-ml/actions/workflows/ci.yml/badge.svg)](https://github.com/EdaNurBinici/izmir-housing-price-ml/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A machine learning-based system for predicting housing prices in Izmir, Turkey, with an integrated luxury scoring algorithm.

## ✨ Features

- 🎯 **Modular Architecture:** Professional-grade code organization
- 📊 **Advanced Data Analysis:** Comprehensive EDA and visualization tools
- 🤖 **Machine Learning:** High-performance HistGradientBoostingRegressor
- 💎 **Luxury Score:** Proprietary algorithm for property valuation
- 🎨 **Modern UI:** Interactive web interface built with Streamlit
- 📝 **Logging System:** Professional logging infrastructure
- ⚙️ **Configuration Management:** YAML-based configuration
- ✅ **Testing Support:** Unit tests for code quality assurance

## 👤 Developer

**Eda Nur Binici**

**Course:** Introduction to Artificial Intelligence

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

### Option 1: Automated Setup (Recommended)

**Windows (PowerShell):**
```powershell
.\scripts\setup.ps1
python model_egitim.py
streamlit run app.py
```

**Linux/Mac:**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
python model_egitim.py
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
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
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

#### 4. Train the Model

```bash
python model_egitim.py
```

This generates model artifacts in the project root:
- `izmir_model.pkl` - Trained HistGradientBoostingRegressor
- `izmir_ilceler.pkl` - District encodings
- `ev_tipleri.pkl` - Property type encodings
- `model_metrikleri.pkl` - Performance metrics (R², MAE, RMSE)
- `model_onem_duzeyleri.pkl` - Feature importance scores
- `ilce_skorlari.pkl` - District target encodings

#### 5. Launch the Application

```bash
streamlit run app.py
```

The application opens automatically at `http://localhost:8501`

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
│   ├── processed/                # Cleaned data files
│   └── data_cleaned.csv          # Main dataset
├── artifacts/                    # Model artifacts (generated)
│   ├── models/                   # Trained models
│   ├── encoders/                 # Encoders and transformers
│   └── metrics/                  # Performance metrics
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
├── Makefile                      # Development commands
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🎯 Usage

### Training the Model

```bash
# Using Make
make train

# Or directly
python model_egitim.py
```

### Running the Application

```bash
# Using Make
make run

# Or directly
streamlit run app.py
```

### Running Tests

```bash
# Using Make
make test

# Or directly
pytest tests/ -v
```

### Code Quality

```bash
# Check code quality
make lint

# Auto-format code
make format
```

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

## 📝 Code Standards

This project follows professional software engineering practices:

- ✅ **Type Hints:** Full type annotation support
- ✅ **Docstrings:** Comprehensive documentation
- ✅ **Modular Architecture:** Clean separation of concerns
- ✅ **Error Handling:** Robust exception management
- ✅ **Logging:** Structured logging system
- ✅ **Testing:** Unit test coverage
- ✅ **Configuration Management:** YAML-based config
- ✅ **Code Formatting:** Black + isort
- ✅ **Linting:** Ruff for code quality
- ✅ **CI/CD:** GitHub Actions pipeline
- ✅ **Pre-commit Hooks:** Automated quality checks
- ✅ **Dependency Pinning:** Reproducible builds

### Code Quality Tools

- **Black:** Code formatting (line length: 100)
- **isort:** Import sorting
- **Ruff:** Fast Python linter
- **pytest:** Testing framework
- **pre-commit:** Git hooks for quality assurance

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

### Model Files Not Found

If the application cannot find model files:

1. Run `model_egitim.py`
2. Ensure all `.pkl` files are in the project root directory

### Configuration File Error

If you encounter config loading errors:

1. Verify `config/config.yaml` exists
2. Check YAML syntax validity

### Log Files

Log files are stored in the `logs/` directory. The directory is created automatically if it doesn't exist.

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

## 🙏 Acknowledgments

We thank the open-source community for the libraries used in this project.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

For questions, please contact the project team or open an issue on GitHub.

---

**Version:** 2.0.0  
**Last Updated:** 2026
