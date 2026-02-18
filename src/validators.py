"""
Data validation module
"""

import logging
from typing import Any, Dict, Optional

import pandas as pd

from .exceptions import ValidationError

logger = logging.getLogger(__name__)


class InputValidator:
    """User input validation class"""

    def __init__(
        self,
        price_min: int = 100000,
        price_max: int = 50000000,
        area_min: int = 20,
        area_max: int = 1000,
        age_min: int = 0,
        age_max: int = 100,
        room_min: int = 1,
        room_max: int = 10,
        salon_min: int = 1,
        salon_max: int = 5,
    ):
        """
        Initializes the validator

        Args:
            price_min: Minimum price
            price_max: Maximum price
            area_min: Minimum area
            area_max: Maximum area
            age_min: Minimum building age
            age_max: Maximum building age
            room_min: Minimum number of rooms
            room_max: Maximum number of rooms
            salon_min: Minimum number of living rooms
            salon_max: Maximum number of living rooms
        """
        self.price_min = price_min
        self.price_max = price_max
        self.area_min = area_min
        self.area_max = area_max
        self.age_min = age_min
        self.age_max = age_max
        self.room_min = room_min
        self.room_max = room_max
        self.salon_min = salon_min
        self.salon_max = salon_max

    def validate_input(
        self,
        ilce: str,
        ev_tipi: str,
        m2: float,
        oda: int,
        salon: int,
        yas: int,
        valid_ilceler: Optional[list] = None,
        valid_tipler: Optional[list] = None,
    ) -> Dict[str, Any]:
        """
        Validates user inputs

        Args:
            ilce: District name
            ev_tipi: Property type
            m2: Area in square meters
            oda: Number of rooms
            salon: Number of living rooms
            yas: Building age
            valid_ilceler: Valid district list
            valid_tipler: Valid property type list

        Returns:
            Validated data

        Raises:
            ValidationError: On validation error
        """
        errors = []

        # District check
        if not ilce or not isinstance(ilce, str):
            errors.append("District cannot be empty")
        elif valid_ilceler and ilce not in valid_ilceler:
            errors.append(f"Invalid district: {ilce}")

        # Property type check
        if not ev_tipi or not isinstance(ev_tipi, str):
            errors.append("Property type cannot be empty")
        elif valid_tipler and ev_tipi not in valid_tipler:
            errors.append(f"Invalid property type: {ev_tipi}")

        # Area check
        if not isinstance(m2, (int, float)) or m2 < self.area_min or m2 > self.area_max:
            errors.append(f"Area must be between {self.area_min}-{self.area_max}")

        # Room count check
        if not isinstance(oda, int) or oda < self.room_min or oda > self.room_max:
            errors.append(f"Number of rooms must be between {self.room_min}-{self.room_max}")

        # Living room count check
        if not isinstance(salon, int) or salon < self.salon_min or salon > self.salon_max:
            errors.append(f"Number of living rooms must be between {self.salon_min}-{self.salon_max}")

        # Building age check
        if not isinstance(yas, int) or yas < self.age_min or yas > self.age_max:
            errors.append(f"Building age must be between {self.age_min}-{self.age_max}")

        if errors:
            error_msg = "; ".join(errors)
            logger.warning(f"Validation error: {error_msg}")
            raise ValidationError(error_msg)

        return {
            "ilce": ilce,
            "ev_tipi": ev_tipi,
            "m2": float(m2),
            "oda": int(oda),
            "salon": int(salon),
            "yas": int(yas),
        }

    def validate_dataframe(self, df: pd.DataFrame, required_columns: list) -> None:
        """
        Validates DataFrame

        Args:
            df: DataFrame to validate
            required_columns: Required columns

        Raises:
            ValidationError: On validation error
        """
        if df.empty:
            raise ValidationError("DataFrame is empty")

        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValidationError(f"Missing columns: {missing_columns}")
