#!/bin/bash
# Setup script for Linux/Mac

echo "Setting up Izmir Housing Price ML project..."

# Create virtual environment
echo -e "\nCreating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo -e "\nActivating virtual environment..."
source venv/bin/activate

# Install dependencies
echo -e "\nInstalling dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo -e "\nSetup complete!"
echo -e "\nNext steps:"
echo "  1. Train the model: python model_egitim.py"
echo "  2. Run the app: streamlit run app.py"
