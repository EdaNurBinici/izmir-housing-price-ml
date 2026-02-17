# Data Directory

This directory contains all data files used in the project.

## Structure

- `raw/` - Original, immutable data files
- `processed/` - Cleaned and processed data ready for modeling

## Files

- `data_cleaned.csv` - Cleaned Izmir housing dataset (6000+ records)

## Data Sources

The dataset contains housing information from Izmir, Turkey including:
- District (ilçe)
- Property type (ev tipi)
- Area in square meters (m²)
- Number of rooms and living rooms
- Building age
- Price

## Usage

Data files are loaded automatically by the application. To regenerate processed data, run:

```bash
python model_egitim.py
```
