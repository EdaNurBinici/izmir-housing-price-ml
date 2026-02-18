"""
Data processing module
"""

import logging

import pandas as pd

from .config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class DataProcessor:
    """Data processing and cleaning class"""

    def __init__(self, config: ConfigLoader):
        """
        Initializes the data processor

        Args:
            config: ConfigLoader instance
        """
        self.config = config
        self.cleaning_config = config.get_cleaning_config()

    def clean_data(self, df: pd.DataFrame, for_training: bool = False) -> pd.DataFrame:
        """
        Cleans the data

        Args:
            df: Raw data DataFrame
            for_training: Is this for model training

        Returns:
            Cleaned DataFrame
        """
        logger.info("Cleaning data...")

        df = df.copy()

        # Clean string columns
        if "district" in df.columns:
            df["district"] = df["district"].astype(str).str.strip().str.title()
        if "left" in df.columns:
            df["left"] = df["left"].astype(str).str.strip().str.title()

        # Calculate total room count
        if "room" in df.columns and "salon" in df.columns:
            df["toplam_oda"] = df["room"] + df["salon"]

        # Determine filtering parameters
        if for_training:
            price_min = self.cleaning_config.get("training_price_min", 300000)
            price_max = self.cleaning_config.get("training_price_max", 35000000)
            area_min = self.cleaning_config.get("training_area_min", 40)
            area_max = self.cleaning_config.get("training_area_max", 450)
        else:
            price_min = self.cleaning_config.get("price_min", 100000)
            price_max = self.cleaning_config.get("price_max", 50000000)
            area_min = self.cleaning_config.get("area_min", 20)
            area_max = self.cleaning_config.get("area_max", 1000)

        # Price filter
        if "price" in df.columns:
            df = df[(df["price"] >= price_min) & (df["price"] <= price_max)]

        # Area filter
        if "area" in df.columns:
            df = df[(df["area"] >= area_min) & (df["area"] <= area_max)]

        logger.info(f"Cleaning completed. Remaining rows: {len(df)}")
        return df

    def get_outlier_stats(self, df: pd.DataFrame) -> dict:
        """
        Returns outlier statistics

        Args:
            df: Raw data DataFrame

        Returns:
            Outlier statistics
        """
        price_min = self.cleaning_config.get("price_min", 100000)
        price_max = self.cleaning_config.get("price_max", 50000000)
        area_min = self.cleaning_config.get("area_min", 20)
        area_max = self.cleaning_config.get("area_max", 1000)

        aykiri_fiyat = df[(df["price"] < price_min) | (df["price"] > price_max)]
        aykiri_m2 = df[(df["area"] < area_min) | (df["area"] > area_max)]

        toplam_atilan_index = aykiri_fiyat.index.union(aykiri_m2.index)
        atilan_sayi = len(toplam_atilan_index)

        temiz_df = self.clean_data(df, for_training=False)

        return {
            "toplam_satir": len(df),
            "atilan_satir": atilan_sayi,
            "kalan_satir": len(temiz_df),
            "price_min": price_min,
            "price_max": price_max,
            "area_min": area_min,
            "area_max": area_max,
        }

    def prepare_eda_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepares data for EDA

        Args:
            df: Raw data DataFrame

        Returns:
            DataFrame prepared for EDA
        """
        clean_df = self.clean_data(df, for_training=False)

        # Additional filters for EDA
        clean_df = clean_df[(clean_df["price"] >= 100000) & (clean_df["price"] <= 25000000)]
        clean_df = clean_df[(clean_df["area"] >= 20) & (clean_df["area"] <= 400)]

        # Additional columns
        if "room" in clean_df.columns and "salon" in clean_df.columns:
            clean_df["toplam_oda"] = clean_df["room"] + clean_df["salon"]
        clean_df["m2_fiyat"] = clean_df["price"] / clean_df["area"]

        return clean_df
