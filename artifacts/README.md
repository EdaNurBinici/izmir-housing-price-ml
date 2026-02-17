# Artifacts Directory

This directory contains all model artifacts and outputs generated during training.

## Structure

- `models/` - Trained model files (.pkl)
- `encoders/` - Encoders and transformers (district lists, property types, scalers)
- `metrics/` - Model performance metrics and evaluation results

## Generated Files

After running `python model_egitim.py`, the following files are created:

### Models
- `izmir_model.pkl` - Trained HistGradientBoostingRegressor model

### Encoders
- `izmir_ilceler.pkl` - List of districts in Izmir
- `ev_tipleri.pkl` - List of property types
- `ilce_skorlari.pkl` - District score mappings (target encoding)

### Metrics
- `model_metrikleri.pkl` - Model performance metrics (R², MAE, RMSE)
- `model_onem_duzeyleri.pkl` - Feature importance scores

## Note

These files are excluded from git (see `.gitignore`) as they can be regenerated from the training script.
