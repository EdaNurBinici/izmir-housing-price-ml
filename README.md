# 🏠 Izmir Housing Price Prediction System

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

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/EdaNurBinici/izmir-housing-price-ml.git
cd izmir-housing-price-ml
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Train the Model

Generate model files:

```bash
python model_egitim.py
```

This command creates:
- `izmir_model.pkl` - Trained model
- `izmir_ilceler.pkl` - District list
- `ev_tipleri.pkl` - Property type list
- `model_metrikleri.pkl` - Model performance metrics
- `model_onem_duzeyleri.pkl` - Feature importance levels
- `ilce_skorlari.pkl` - District scores

### 5. Launch the Application

```bash
streamlit run app.py
```

The application will automatically open in your browser (typically at `http://localhost:8501`).

## 📁 Project Structure

```
izmir-housing-price-ml/
├── src/                      # Source code modules
│   ├── __init__.py
│   ├── config_loader.py     # YAML configuration loader
│   ├── logger_setup.py       # Logging system
│   ├── exceptions.py         # Custom exceptions
│   ├── validators.py         # Data validation
│   ├── model_loader.py       # Model loading
│   ├── luxury_score.py       # Luxury score calculation
│   ├── predictor.py          # Price prediction
│   ├── data_processor.py    # Data processing
│   └── train_model.py        # Model training module
├── config/                   # Configuration files
│   └── config.yaml           # Main configuration
├── tests/                    # Test files
│   ├── __init__.py
│   ├── test_validators.py
│   └── test_luxury_score.py
├── logs/                     # Log files (auto-generated)
├── app.py                    # Streamlit application
├── model_egitim.py           # Model training script
├── grafik.py                 # Visualization script
├── data_cleaned.csv          # Cleaned dataset
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore file
└── README.md                 # This file
```

## 🎯 Usage

### Model Training

```bash
python model_egitim.py
```

### Run Application

```bash
streamlit run app.py
```

### Run Tests

```bash
pytest tests/ -v
```

## 📊 Model Performance

Model performance metrics are displayed after running `model_egitim.py`:

- **R² Score:** Model accuracy indicator
- **MAE:** Mean Absolute Error
- **RMSE:** Root Mean Square Error

## 🔧 Configuration

All configuration settings are in `config/config.yaml`:

- Data file paths
- Model parameters
- Data cleaning thresholds
- Luxury score parameters
- Logging settings

## 📝 Code Standards

This project follows professional coding standards:

- ✅ Type hints
- ✅ Comprehensive docstrings
- ✅ Modular architecture
- ✅ Error handling
- ✅ Logging infrastructure
- ✅ Unit tests
- ✅ Configuration management

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

## 📞 Contact

For questions, please contact the project team.

---

**Version:** 2.0.0  
**Last Updated:** 2026
