"""
preprocessing.py
Data preprocessing, meteorological feature engineering, lag creation,
and chronological dataset splitting for 1 to 3-day ahead rainfall forecasting.
"""

import numpy as np
import pandas as pd
from typing import Tuple, List, Dict, Optional


def load_openmeteo_csv(filepath: str) -> pd.DataFrame:
    """
    Loads Open-Meteo CSV file, skipping the metadata header lines.
    Standardizes column names and parses datetime.
    """
    df = pd.read_csv(filepath, skiprows=3)
    
    # Clean column names
    column_mapping = {
        'time': 'timestamp',
        'temperature_2m (°C)': 'temperature',
        'surface_pressure (hPa)': 'surface_pressure',
        'relative_humidity_2m (%)': 'relative_humidity',
        'cloud_cover (%)': 'cloud_cover',
        'wind_direction_10m (°)': 'wind_direction_10m',
        'rain (mm)': 'rain',
        'wind_speed_10m (km/h)': 'wind_speed_10m',
        'wind_speed_100m (km/h)': 'wind_speed_100m',
        'wind_direction_100m (°)': 'wind_direction_100m'
    }
    
    # Handle special character encodings
    new_cols = []
    for col in df.columns:
        matched = False
        for k, v in column_mapping.items():
            if k.split()[0] in col:
                new_cols.append(v)
                matched = True
                break
        if not matched:
            new_cols.append(col.strip().lower().replace(' ', '_'))
    
    df.columns = new_cols
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)
    return df


def calculate_atmospheric_indices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Derives physical atmospheric indicators:
    - Dew Point Temperature (°C) via Magnus formula
    - Vapor Pressure Deficit (VPD in kPa)
    - Relative Humidity / Temperature interaction
    - Pressure 24h tendency (barometric change rate)
    """
    data = df.copy()
    
    # Magnus-Tetens approximation for Dew Point:
    # T_dew = (b * alpha) / (a - alpha), where alpha = (a*T)/(b+T) + ln(RH/100)
    a = 17.27
    b = 237.7
    t = data['temperature']
    rh = data['relative_humidity'].clip(lower=1.0, upper=100.0)
    
    alpha = ((a * t) / (b + t)) + np.log(rh / 100.0)
    data['dew_point'] = (b * alpha) / (a - alpha)
    
    # Dew Point Depression (T - T_dew): smaller gap indicates saturated air / high rain probability
    data['dew_point_depression'] = t - data['dew_point']
    
    # Saturation Vapor Pressure (e_s in kPa) and Actual Vapor Pressure (e_a in kPa)
    e_s = 0.61078 * np.exp((17.27 * t) / (t + 237.3))
    e_a = e_s * (rh / 100.0)
    data['vapor_pressure_deficit'] = e_s - e_a  # VPD
    
    # Pressure 6h, 12h, and 24h tendencies (falling pressure often signals storm fronts)
    data['pressure_tendency_6h'] = data['surface_pressure'] - data['surface_pressure'].shift(6)
    data['pressure_tendency_24h'] = data['surface_pressure'] - data['surface_pressure'].shift(24)
    
    # Wind vector components (u = East-West, v = North-South)
    if 'wind_direction_10m' in data.columns and 'wind_speed_10m' in data.columns:
        rad = np.deg2rad(data['wind_direction_10m'])
        data['wind_u_10m'] = -data['wind_speed_10m'] * np.sin(rad)
        data['wind_v_10m'] = -data['wind_speed_10m'] * np.cos(rad)
        
    return data


def add_cyclical_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encodes temporal periodicity using Sine and Cosine transformations:
    - Hour of day (24-hour cycle)
    - Day of year (365-day seasonal cycle)
    - Month of year (12-month monsoon cycle)
    """
    data = df.copy()
    ts = data['timestamp']
    
    # Hour cycle
    hour = ts.dt.hour
    data['sin_hour'] = np.sin(2 * np.pi * hour / 24.0)
    data['cos_hour'] = np.cos(2 * np.pi * hour / 24.0)
    
    # Day of year (Monsoon seasonality in South Asia)
    doy = ts.dt.dayofyear
    data['sin_doy'] = np.sin(2 * np.pi * doy / 365.25)
    data['cos_doy'] = np.cos(2 * np.pi * doy / 365.25)
    
    # Month cycle
    month = ts.dt.month
    data['sin_month'] = np.sin(2 * np.pi * month / 12.0)
    data['cos_month'] = np.cos(2 * np.pi * month / 12.0)
    
    return data


def generate_lagged_and_rolling_features(df: pd.DataFrame, 
                                         lag_hours: List[int] = [1, 2, 3, 6, 12, 24, 48, 72],
                                         rolling_windows: List[int] = [6, 12, 24, 48, 72]) -> pd.DataFrame:
    """
    Creates historical lag features and rolling aggregations (mean, std, max, sum)
    for weather parameters to capture short-term and multi-day meteorological memory.
    """
    data = df.copy()
    
    base_features = ['temperature', 'relative_humidity', 'surface_pressure', 
                     'cloud_cover', 'rain', 'wind_speed_10m', 'dew_point_depression']
    
    # Available base features in dataset
    available_base = [col for col in base_features if col in data.columns]
    
    # Lagged features
    for col in available_base:
        for lag in lag_hours:
            data[f'{col}_lag_{lag}h'] = data[col].shift(lag)
            
    # Rolling aggregations
    for col in available_base:
        for w in rolling_windows:
            data[f'{col}_roll_mean_{w}h'] = data[col].shift(1).rolling(window=w, min_periods=max(1, w//2)).mean()
            data[f'{col}_roll_max_{w}h'] = data[col].shift(1).rolling(window=w, min_periods=max(1, w//2)).max()
            if col == 'rain':
                # Cumulative rainfall over window
                data[f'rain_roll_sum_{w}h'] = data['rain'].shift(1).rolling(window=w, min_periods=max(1, w//2)).sum()
                
    return data


def construct_multi_day_targets(df: pd.DataFrame, rain_threshold_mm: float = 1.0) -> pd.DataFrame:
    """
    Constructs multi-step forecasting targets for 1 to 3 days ahead:
    - Day +1 (Next 1-24 hours cumulative rain in mm)
    - Day +2 (Hours 25-48 cumulative rain in mm)
    - Day +3 (Hours 49-72 cumulative rain in mm)
    - Binary classification targets (Will it rain > threshold on Day +1, Day +2, Day +3?)
    - Multi-class risk targets: 0 = No Rain (<1mm), 1 = Light/Moderate (1-15mm), 2 = Heavy/Flood (>15mm)
    """
    data = df.copy()
    
    # Future 24h rolling sum: shift(-24)
    # Target 1: Day +1 (next 24 hours)
    data['target_rain_day1_mm'] = data['rain'].iloc[::-1].rolling(window=24, min_periods=24).sum().iloc[::-1].shift(-1)
    
    # Target 2: Day +2 (25 to 48 hours ahead)
    data['target_rain_day2_mm'] = data['rain'].iloc[::-1].rolling(window=24, min_periods=24).sum().iloc[::-1].shift(-25)
    
    # Target 3: Day +3 (49 to 72 hours ahead)
    data['target_rain_day3_mm'] = data['rain'].iloc[::-1].rolling(window=24, min_periods=24).sum().iloc[::-1].shift(-49)
    
    # Binary Classification: Rain Occurrence (1 = Yes, 0 = No)
    data['target_class_day1'] = (data['target_rain_day1_mm'] >= rain_threshold_mm).astype(float)
    data['target_class_day2'] = (data['target_rain_day2_mm'] >= rain_threshold_mm).astype(float)
    data['target_class_day3'] = (data['target_rain_day3_mm'] >= rain_threshold_mm).astype(float)
    
    # Categorical Risk Level: 0=None (<1mm), 1=Moderate (1-15mm), 2=Heavy (>15mm)
    def categorize_rain(val):
        if pd.isna(val):
            return np.nan
        if val < 1.0:
            return 0  # No Rain
        elif val <= 15.0:
            return 1  # Moderate Rain
        else:
            return 2  # Heavy Rain
            
    data['target_risk_day1'] = data['target_rain_day1_mm'].apply(categorize_rain)
    data['target_risk_day2'] = data['target_rain_day2_mm'].apply(categorize_rain)
    data['target_risk_day3'] = data['target_rain_day3_mm'].apply(categorize_rain)
    
    return data


def chronological_train_val_test_split(
    df: pd.DataFrame, 
    train_ratio: float = 0.70, 
    val_ratio: float = 0.15, 
    test_ratio: float = 0.15
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Performs strict chronological splitting (time-series split) to prevent data leakage.
    Train: Earliest data (e.g., 2023 - 2024)
    Val: Middle data (e.g., 2025)
    Test: Most recent data (e.g., 2026)
    """
    assert np.isclose(train_ratio + val_ratio + test_ratio, 1.0), "Ratios must sum to 1.0"
    
    # Drop rows with NaN values resulting from lags or lead targets
    clean_df = df.dropna().reset_index(drop=True)
    
    n = len(clean_df)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))
    
    train_df = clean_df.iloc[:train_end].copy().reset_index(drop=True)
    val_df = clean_df.iloc[train_end:val_end].copy().reset_index(drop=True)
    test_df = clean_df.iloc[val_end:].copy().reset_index(drop=True)
    
    return train_df, val_df, test_df


def prepare_features_and_targets(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, pd.Series]]:
    """
    Separates feature matrix X from all regression and classification target sets.
    """
    target_cols = [
        'target_rain_day1_mm', 'target_rain_day2_mm', 'target_rain_day3_mm',
        'target_class_day1', 'target_class_day2', 'target_class_day3',
        'target_risk_day1', 'target_risk_day2', 'target_risk_day3'
    ]
    non_feature_cols = ['timestamp'] + target_cols
    
    feature_cols = [c for c in df.columns if c not in non_feature_cols]
    
    X = df[feature_cols].copy()
    targets = {
        'regression': df[['target_rain_day1_mm', 'target_rain_day2_mm', 'target_rain_day3_mm']].copy(),
        'classification_binary': df[['target_class_day1', 'target_class_day2', 'target_class_day3']].copy(),
        'classification_risk': df[['target_risk_day1', 'target_risk_day2', 'target_risk_day3']].copy()
    }
    
    return X, targets
