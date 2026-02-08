"""
Time Series Analysis Module
===========================
Implements statistical tests and analysis for time series data:
- Stationarity tests (ADF, KPSS)
- Volatility calculations
- Autocorrelation analysis
- Rolling statistics
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.stats.diagnostic import het_arch
import logging

logger = logging.getLogger(__name__)


class StationarityTestError(Exception):
    """Custom exception for stationarity test errors."""
    pass


def adf_test(series: pd.Series, 
             regression: str = 'c',
             maxlag: Optional[int] = None,
             autolag: str = 'AIC') -> Dict:
    """
    Perform Augmented Dickey-Fuller test for stationarity.
    
    H0: Unit root present (non-stationary)
    H1: Stationary
    
    Parameters
    ----------
    series : pd.Series
        Time series to test.
    regression : str
        Regression type: 'c' (constant), 'ct' (constant+trend), 'ctt', 'n' (none).
    maxlag : int, optional
        Maximum lag to use. If None, uses int(12*(nobs/100)**(1/4)).
    autolag : str
        Method for lag selection ('AIC', 'BIC', 't-stat').
    
    Returns
    -------
    Dict
        Test results including:
        - test_statistic: ADF test statistic
        - p_value: p-value
        - usedlag: Number of lags used
        - nobs: Number of observations
        - critical_values: Critical values at 1%, 5%, 10%
        - ic_best: Best information criterion if autolag
        - is_stationary: Boolean interpretation
    """
    try:
        logger.info(f"Running ADF test with regression='{regression}'")
        
        # Remove NaN values
        clean_series = series.dropna()
        
        if len(clean_series) < 10:
            raise StationarityTestError("Insufficient data for ADF test (need >= 10 observations)")
        
        # Perform test
        result = adfuller(clean_series, regression=regression, 
                         maxlag=maxlag, autolag=autolag)
        
        # Format results
        test_stat = result[0]
        p_value = result[1]
        usedlag = result[2]
        nobs = result[3]
        critical_values = result[4]
        icbest = result[5] if len(result) > 5 else None
        
        # Interpretation
        is_stationary = p_value < 0.05
        
        results = {
            'test': 'ADF',
            'regression': regression,
            'test_statistic': test_stat,
            'p_value': p_value,
            'used_lag': usedlag,
            'n_observations': nobs,
            'critical_values': critical_values,
            'ic_best': icbest,
            'is_stationary': is_stationary,
            'interpretation': 'Stationary' if is_stationary else 'Non-stationary',
            'conclusion': (
                f"Reject H0 (stationary)" if is_stationary 
                else f"Fail to reject H0 (non-stationary, unit root present)"
            )
        }
        
        logger.info(f"ADF Test: test_stat={test_stat:.4f}, p_value={p_value:.4f}, "
                   f"result={results['interpretation']}")
        
        return results
    
    except Exception as e:
        raise StationarityTestError(f"ADF test failed: {e}")


def kpss_test(series: pd.Series,
             regression: str = 'c',
             nlags: str = 'auto') -> Dict:
    """
    Perform Kwiatkowski-Phillips-Schmidt-Shin test for stationarity.
    
    H0: Stationary (around constant or trend)
    H1: Unit root present (non-stationary)
    
    Parameters
    ----------
    series : pd.Series
        Time series to test.
    regression : str
        'c' for stationarity around constant, 'ct' around trend.
    nlags : str or int
        Lag selection ('auto', 'legacy', or int).
    
    Returns
    -------
    Dict
        Test results including:
        - test_statistic: KPSS test statistic
        - p_value: p-value
        - lags: Number of lags used
        - critical_values: Critical values
        - is_stationary: Boolean interpretation
    """
    try:
        logger.info(f"Running KPSS test with regression='{regression}'")
        
        # Remove NaN values
        clean_series = series.dropna()
        
        if len(clean_series) < 10:
            raise StationarityTestError("Insufficient data for KPSS test (need >= 10 observations)")
        
        # Perform test
        result = kpss(clean_series, regression=regression, nlags=nlags)
        
        test_stat = result[0]
        p_value = result[1]
        lags = result[2]
        critical_values = result[3]
        
        # Interpretation (note: opposite of ADF)
        is_stationary = p_value > 0.05
        
        results = {
            'test': 'KPSS',
            'regression': regression,
            'test_statistic': test_stat,
            'p_value': p_value,
            'lags': lags,
            'critical_values': critical_values,
            'is_stationary': is_stationary,
            'interpretation': 'Stationary' if is_stationary else 'Non-stationary',
            'conclusion': (
                f"Fail to reject H0 (stationary)" if is_stationary 
                else f"Reject H0 (non-stationary, unit root present)"
            )
        }
        
        logger.info(f"KPSS Test: test_stat={test_stat:.4f}, p_value={p_value:.4f}, "
                   f"result={results['interpretation']}")
        
        return results
    
    except Exception as e:
        raise StationarityTestError(f"KPSS test failed: {e}")


def run_stationarity_tests(series: pd.Series, 
                          name: str = "series") -> Dict[str, Dict]:
    """
    Run both ADF and KPSS tests on a series.
    
    Parameters
    ----------
    series : pd.Series
        Time series to test.
    name : str
        Name identifier for the series.
    
    Returns
    -------
    Dict
        Results from both tests with consolidated interpretation.
    """
    logger.info(f"Running stationarity tests on {name}")
    
    results = {
        'series_name': name,
        'adf': None,
        'kpss': None,
        'consensus': None
    }
    
    # ADF test (constant)
    results['adf'] = adf_test(series, regression='c')
    
    # KPSS test (constant)
    results['kpss'] = kpss_test(series, regression='c')
    
    # Consensus interpretation
    adf_stationary = results['adf']['is_stationary']
    kpss_stationary = results['kpss']['is_stationary']
    
    if adf_stationary and kpss_stationary:
        consensus = "Stationary"
    elif not adf_stationary and not kpss_stationary:
        consensus = "Non-stationary (unit root)"
    elif not adf_stationary and kpss_stationary:
        consensus = "Difference stationary (may need differencing)"
    else:  # ADF says stationary, KPSS says non-stationary
        consensus = "Trend stationary (deterministic trend)"
    
    results['consensus'] = {
        'classification': consensus,
        'adf_result': 'Stationary' if adf_stationary else 'Non-stationary',
        'kpss_result': 'Stationary' if kpss_stationary else 'Non-stationary',
        'recommendation': _get_recommendation(consensus)
    }
    
    logger.info(f"Consensus: {consensus}")
    
    return results


def _get_recommendation(classification: str) -> str:
    """Get modeling recommendation based on classification."""
    recommendations = {
        "Stationary": "Use series directly in ARMA models",
        "Non-stationary (unit root)": "Apply differencing (ARIMA models)",
        "Difference stationary (may need differencing)": "Apply differencing and retest",
        "Trend stationary (deterministic trend)": "Detrend series (remove deterministic trend)"
    }
    return recommendations.get(classification, "Further analysis needed")


def compute_volatility(df: pd.DataFrame,
                      windows: list = [30, 60, 90],
                      use_log_returns: bool = True) -> pd.DataFrame:
    """
    Compute rolling volatility statistics.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with returns column.
    windows : list
        List of rolling window sizes (days).
    use_log_returns : bool
        Whether to use log returns (True) or simple returns (False).
    
    Returns
    -------
    pd.DataFrame
        DataFrame with added volatility columns.
    """
    logger.info(f"Computing volatility with windows: {windows}")
    
    df_result = df.copy()
    
    # Determine return column
    return_col = 'Log_Returns' if use_log_returns and 'Log_Returns' in df.columns else 'Simple_Returns'
    
    if return_col not in df.columns:
        raise ValueError(f"Return column '{return_col}' not found. Compute returns first.")
    
    returns = df_result[return_col].dropna()
    
    for window in windows:
        # Annualized volatility (std dev * sqrt(trading days))
        col_name = f'Volatility_{window}d'
        df_result[col_name] = returns.rolling(window=window).std() * np.sqrt(252)
    
    # Average volatility across all windows
    vol_cols = [f'Volatility_{w}d' for w in windows]
    df_result['Avg_Volatility'] = df_result[vol_cols].mean(axis=1)
    
    logger.info(f"Added {len(windows)} volatility columns")
    
    return df_result


def detect_volatility_regimes(df: pd.DataFrame,
                             vol_col: str = 'Avg_Volatility',
                             method: str = 'quantile') -> pd.DataFrame:
    """
    Classify periods into volatility regimes.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with volatility column.
    vol_col : str
        Column name for volatility measure.
    method : str
        Classification method ('quantile', 'std', 'manual').
    
    Returns
    -------
    pd.DataFrame
        DataFrame with added regime classification.
    """
    logger.info(f"Detecting volatility regimes using {method} method")
    
    df_result = df.copy()
    volatility = df_result[vol_col].dropna()
    
    if method == 'quantile':
        # Classify by quantiles
        low_threshold = volatility.quantile(0.33)
        high_threshold = volatility.quantile(0.67)
        
        def classify(vol):
            if pd.isna(vol):
                return 'Unknown'
            elif vol < low_threshold:
                return 'Low'
            elif vol > high_threshold:
                return 'High'
            else:
                return 'Medium'
    
    elif method == 'std':
        mean_vol = volatility.mean()
        std_vol = volatility.std()
        
        def classify(vol):
            if pd.isna(vol):
                return 'Unknown'
            elif vol < mean_vol - 0.5 * std_vol:
                return 'Low'
            elif vol > mean_vol + 0.5 * std_vol:
                return 'High'
            else:
                return 'Medium'
    
    else:
        raise ValueError(f"Unknown method: {method}")
    
    df_result['Volatility_Regime'] = df_result[vol_col].apply(classify)
    
    # Log regime distribution
    regime_counts = df_result['Volatility_Regime'].value_counts()
    logger.info(f"Regime distribution: {dict(regime_counts)}")
    
    return df_result


def compute_rolling_statistics(df: pd.DataFrame,
                              price_col: str = 'Price',
                              windows: list = [30, 60, 90, 252]) -> pd.DataFrame:
    """
    Compute rolling mean, std, min, max statistics.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with price column.
    price_col : str
        Name of price column.
    windows : list
        List of window sizes.
    
    Returns
    -------
    pd.DataFrame
        DataFrame with added rolling statistics.
    """
    logger.info(f"Computing rolling statistics with windows: {windows}")
    
    df_result = df.copy()
    prices = df_result[price_col]
    
    for window in windows:
        df_result[f'MA_{window}'] = prices.rolling(window=window).mean()
        df_result[f'Std_{window}'] = prices.rolling(window=window).std()
        df_result[f'Min_{window}'] = prices.rolling(window=window).min()
        df_result[f'Max_{window}'] = prices.rolling(window=window).max()
    
    # Bollinger Bands (20-day)
    df_result['BB_Middle'] = prices.rolling(window=20).mean()
    bb_std = prices.rolling(window=20).std()
    df_result['BB_Upper'] = df_result['BB_Middle'] + (2 * bb_std)
    df_result['BB_Lower'] = df_result['BB_Middle'] - (2 * bb_std)
    
    logger.info("Added rolling statistics and Bollinger Bands")
    
    return df_result


def test_arch_effects(returns: pd.Series, 
                     max_lag: int = 5) -> Dict:
    """
    Test for ARCH effects (volatility clustering) in returns.
    
    Parameters
    ----------
    returns : pd.Series
        Return series.
    max_lag : int
        Maximum lag for ARCH test.
    
    Returns
    -------
    Dict
        Test results including LM statistic and p-value.
    """
    try:
        logger.info(f"Testing for ARCH effects (max_lag={max_lag})")
        
        clean_returns = returns.dropna()
        
        # ARCH test
        lm_stat, lm_pvalue, f_stat, f_pvalue = het_arch(clean_returns, maxlag=max_lag)
        
        has_arch = lm_pvalue < 0.05
        
        results = {
            'lm_statistic': lm_stat,
            'lm_pvalue': lm_pvalue,
            'f_statistic': f_stat,
            'f_pvalue': f_pvalue,
            'max_lag': max_lag,
            'has_arch_effects': has_arch,
            'interpretation': (
                'ARCH effects detected (volatility clustering)' if has_arch 
                else 'No ARCH effects detected'
            )
        }
        
        logger.info(f"ARCH Test: LM={lm_stat:.4f}, p={lm_pvalue:.4f}, "
                   f"result={results['interpretation']}")
        
        return results
    
    except Exception as e:
        logger.error(f"ARCH test failed: {e}")
        return {
            'error': str(e),
            'has_arch_effects': None
        }


if __name__ == "__main__":
    # Example usage
    from data_loader import load_brent_data, compute_log_returns
    
    try:
        # Load and prepare data
        df = load_brent_data("../data/raw/BrentOilPrices.csv")
        df_clean = df.copy()  # Assume already cleaned
        df_returns = compute_log_returns(df_clean)
        
        # Stationarity tests
        price_results = run_stationarity_tests(df_clean['Price'], "Price Levels")
        print("\n=== PRICE LEVEL STATIONARITY ===")
        print(f"ADF: {price_results['adf']['interpretation']} (p={price_results['adf']['p_value']:.4f})")
        print(f"KPSS: {price_results['kpss']['interpretation']} (p={price_results['kpss']['p_value']:.4f})")
        print(f"Consensus: {price_results['consensus']['classification']}")
        
        return_results = run_stationarity_tests(df_returns['Log_Returns'].dropna(), "Log Returns")
        print("\n=== RETURN STATIONARITY ===")
        print(f"ADF: {return_results['adf']['interpretation']} (p={return_results['adf']['p_value']:.4f})")
        print(f"KPSS: {return_results['kpss']['interpretation']} (p={return_results['kpss']['p_value']:.4f})")
        print(f"Consensus: {return_results['consensus']['classification']}")
        
        # Volatility analysis
        df_vol = compute_volatility(df_returns)
        df_regimes = detect_volatility_regimes(df_vol)
        
        print("\n=== VOLATILITY REGIMES ===")
        print(df_regimes['Volatility_Regime'].value_counts())
        
        # ARCH test
        arch_results = test_arch_effects(df_returns['Log_Returns'])
        print(f"\n=== ARCH EFFECTS ===")
        print(f"{arch_results['interpretation']} (p={arch_results['lm_pvalue']:.4f})")
        
    except Exception as e:
        logger.error(f"Error in analysis: {e}")
