"""
Data Loading and Validation Module
====================================
Handles loading, cleaning, and validation of Brent oil price data.
Provides robust error handling and data quality checks.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional, Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DataLoadError(Exception):
    """Custom exception for data loading errors."""
    pass


class DataValidationError(Exception):
    """Custom exception for data validation errors."""
    pass


def load_brent_data(file_path: str) -> pd.DataFrame:
    """
    Load Brent oil price data from CSV file.
    
    Parameters
    ----------
    file_path : str
        Path to the CSV file containing Brent oil price data.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with 'Date' as index and 'Price' column.
    
    Raises
    ------
    DataLoadError
        If file not found or cannot be loaded.
    """
    try:
        path = Path(file_path)
        if not path.exists():
            raise DataLoadError(f"Data file not found: {file_path}")
        
        logger.info(f"Loading data from {file_path}")
        
        # Load CSV with flexible column name handling
        df = pd.read_csv(file_path)
        
        # Standardize column names (handle common variations)
        column_mapping = {
            'date': 'Date',
            'DATE': 'Date',
            'Date': 'Date',
            'price': 'Price',
            'PRICE': 'Price',
            'Price': 'Price',
            'Close': 'Price',
            'close': 'Price',
            'Brent': 'Price',
            'brent': 'Price'
        }
        
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
        
        if 'Date' not in df.columns:
            raise DataLoadError(f"Required 'Date' column not found. Available columns: {list(df.columns)}")
        if 'Price' not in df.columns:
            raise DataLoadError(f"Required 'Price' column not found. Available columns: {list(df.columns)}")
        
        # Parse dates and set index
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.set_index('Date').sort_index()
        
        # Ensure Price is numeric
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        
        logger.info(f"Successfully loaded {len(df)} records spanning {df.index.min()} to {df.index.max()}")
        
        return df[['Price']]
    
    except pd.errors.EmptyDataError:
        raise DataLoadError(f"File is empty: {file_path}")
    except pd.errors.ParserError as e:
        raise DataLoadError(f"Error parsing CSV file: {e}")
    except Exception as e:
        raise DataLoadError(f"Unexpected error loading data: {e}")


def validate_data(df: pd.DataFrame, 
                  max_missing_pct: float = 0.05,
                  max_consecutive_missing: int = 5) -> Dict[str, any]:
    """
    Validate data quality and completeness.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 'Price' column.
    max_missing_pct : float
        Maximum acceptable percentage of missing values (default 5%).
    max_consecutive_missing : int
        Maximum acceptable consecutive missing values (default 5).
    
    Returns
    -------
    Dict
        Validation results with status and details.
    
    Raises
    ------
    DataValidationError
        If validation criteria are not met.
    """
    logger.info("Validating data quality...")
    
    results = {
        'is_valid': True,
        'missing_count': 0,
        'missing_pct': 0.0,
        'consecutive_gaps': [],
        'outliers': 0,
        'negative_prices': 0,
        'date_range': None,
        'warnings': [],
        'errors': []
    }
    
    # Check for missing values
    missing_count = df['Price'].isna().sum()
    missing_pct = missing_count / len(df) * 100
    results['missing_count'] = missing_count
    results['missing_pct'] = missing_pct
    
    if missing_pct > max_missing_pct:
        msg = f"Missing values exceed threshold: {missing_pct:.2f}% > {max_missing_pct*100}%"
        results['errors'].append(msg)
        results['is_valid'] = False
    elif missing_count > 0:
        results['warnings'].append(f"Found {missing_count} missing values ({missing_pct:.2f}%)")
    
    # Check for consecutive missing values
    if missing_count > 0:
        is_missing = df['Price'].isna()
        gaps = []
        current_gap = 0
        
        for is_miss in is_missing:
            if is_miss:
                current_gap += 1
            else:
                if current_gap > 0:
                    gaps.append(current_gap)
                current_gap = 0
        if current_gap > 0:
            gaps.append(current_gap)
        
        long_gaps = [g for g in gaps if g > max_consecutive_missing]
        results['consecutive_gaps'] = long_gaps
        
        if long_gaps:
            msg = f"Found {len(long_gaps)} gaps exceeding {max_consecutive_missing} consecutive days"
            results['errors'].append(msg)
            results['is_valid'] = False
    
    # Check for negative or zero prices
    invalid_prices = (df['Price'] <= 0).sum()
    results['negative_prices'] = invalid_prices
    
    if invalid_prices > 0:
        msg = f"Found {invalid_prices} non-positive price values"
        results['errors'].append(msg)
        results['is_valid'] = False
    
    # Check for outliers (prices outside reasonable range)
    # Brent crude historical range: $10 - $150
    outliers = ((df['Price'] < 10) | (df['Price'] > 150)).sum()
    results['outliers'] = outliers
    
    if outliers > 0:
        results['warnings'].append(f"Found {outliers} prices outside typical range ($10-$150)")
    
    # Date range
    results['date_range'] = (df.index.min(), df.index.max())
    
    # Summary
    if results['is_valid']:
        logger.info("Data validation passed")
    else:
        logger.warning("Data validation failed")
        for error in results['errors']:
            logger.error(f"  - {error}")
    
    for warning in results['warnings']:
        logger.warning(f"  - {warning}")
    
    return results


def clean_data(df: pd.DataFrame, 
               fill_method: str = 'linear',
               remove_outliers: bool = False,
               outlier_threshold: float = 3.0) -> pd.DataFrame:
    """
    Clean and preprocess the price data.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 'Price' column.
    fill_method : str
        Method for filling missing values ('linear', 'ffill', 'bfill', 'none').
    remove_outliers : bool
        Whether to remove statistical outliers.
    outlier_threshold : float
        Number of standard deviations for outlier detection.
    
    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame.
    """
    logger.info(f"Cleaning data with fill_method='{fill_method}'")
    
    df_clean = df.copy()
    
    # Handle missing values
    if fill_method == 'linear':
        df_clean['Price'] = df_clean['Price'].interpolate(method='linear')
    elif fill_method == 'ffill':
        df_clean['Price'] = df_clean['Price'].fillna(method='ffill').fillna(method='bfill')
    elif fill_method == 'bfill':
        df_clean['Price'] = df_clean['Price'].fillna(method='bfill').fillna(method='ffill')
    # else: 'none' - don't fill
    
    # Remove outliers if requested
    if remove_outliers:
        mean_price = df_clean['Price'].mean()
        std_price = df_clean['Price'].std()
        threshold = outlier_threshold * std_price
        
        outlier_mask = (df_clean['Price'] < mean_price - threshold) | \
                       (df_clean['Price'] > mean_price + threshold)
        outlier_count = outlier_mask.sum()
        
        if outlier_count > 0:
            logger.info(f"Removing {outlier_count} outliers (>{outlier_threshold} std devs)")
            df_clean = df_clean[~outlier_mask]
    
    logger.info(f"Data cleaning complete. Final shape: {df_clean.shape}")
    
    return df_clean


def compute_log_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute log returns from price data.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 'Price' column.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with 'Price' and 'Log_Returns' columns.
    """
    logger.info("Computing log returns")
    
    df_result = df.copy()
    
    # Calculate log returns: ln(P_t / P_{t-1})
    df_result['Log_Returns'] = np.log(df_result['Price'] / df_result['Price'].shift(1))
    
    # First value will be NaN (no previous price)
    returns_count = df_result['Log_Returns'].notna().sum()
    logger.info(f"Computed {returns_count} log returns")
    
    return df_result


def compute_simple_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute simple returns from price data.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 'Price' column.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with 'Price' and 'Simple_Returns' columns.
    """
    logger.info("Computing simple returns")
    
    df_result = df.copy()
    df_result['Simple_Returns'] = df_result['Price'].pct_change()
    
    returns_count = df_result['Simple_Returns'].notna().sum()
    logger.info(f"Computed {returns_count} simple returns")
    
    return df_result


def load_events_data(file_path: str) -> pd.DataFrame:
    """
    Load geopolitical events data.
    
    Parameters
    ----------
    file_path : str
        Path to events CSV file.
    
    Returns
    -------
    pd.DataFrame
        Events DataFrame with 'Event_Date' as index.
    """
    try:
        path = Path(file_path)
        if not path.exists():
            raise DataLoadError(f"Events file not found: {file_path}")
        
        logger.info(f"Loading events data from {file_path}")
        
        df = pd.read_csv(file_path)
        
        # Parse dates
        if 'Event_Date' in df.columns:
            df['Event_Date'] = pd.to_datetime(df['Event_Date'], errors='coerce')
            df = df.set_index('Event_Date').sort_index()
        
        logger.info(f"Loaded {len(df)} events spanning {df.index.min()} to {df.index.max()}")
        
        return df
    
    except Exception as e:
        raise DataLoadError(f"Error loading events data: {e}")


if __name__ == "__main__":
    # Example usage
    try:
        # Load data
        data_path = "../data/raw/BrentOilPrices.csv"
        df = load_brent_data(data_path)
        
        # Validate
        validation = validate_data(df)
        print(f"Validation results: {validation}")
        
        # Clean
        df_clean = clean_data(df, fill_method='linear')
        
        # Compute returns
        df_returns = compute_log_returns(df_clean)
        
        print(f"\nData summary:")
        print(df_returns.describe())
        
    except Exception as e:
        logger.error(f"Error in data processing: {e}")
