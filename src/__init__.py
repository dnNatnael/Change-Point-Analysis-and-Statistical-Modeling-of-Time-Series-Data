"""
Brent Oil Price Analysis - Source Modules
=========================================

This package contains modular Python code for analyzing Brent oil price time series data.

Modules:
- data_loader: Data loading, validation, and preprocessing
- time_series_analysis: Statistical tests (ADF, KPSS), volatility analysis
- visualization: Plotting functions for trends, volatility, and diagnostics

Usage:
    from src import load_brent_data, run_stationarity_tests
    from src import plot_price_trend, plot_volatility_analysis
"""

from .data_loader import (
    load_brent_data,
    validate_data,
    clean_data,
    compute_log_returns,
    compute_simple_returns,
    load_events_data,
    DataLoadError,
    DataValidationError
)

from .time_series_analysis import (
    adf_test,
    kpss_test,
    run_stationarity_tests,
    compute_volatility,
    detect_volatility_regimes,
    compute_rolling_statistics,
    test_arch_effects,
    StationarityTestError
)

from .visualization import (
    plot_price_trend,
    plot_returns_distribution,
    plot_volatility_analysis,
    plot_stationarity_diagnostics,
    plot_events_overlay,
    VisualizationError
)

__version__ = "1.0.0"
__author__ = "Data Analysis Team"

__all__ = [
    # Data loading
    'load_brent_data',
    'validate_data',
    'clean_data',
    'compute_log_returns',
    'compute_simple_returns',
    'load_events_data',
    # Time series analysis
    'adf_test',
    'kpss_test',
    'run_stationarity_tests',
    'compute_volatility',
    'detect_volatility_regimes',
    'compute_rolling_statistics',
    'test_arch_effects',
    # Visualization
    'plot_price_trend',
    'plot_returns_distribution',
    'plot_volatility_analysis',
    'plot_stationarity_diagnostics',
    'plot_events_overlay',
    # Exceptions
    'DataLoadError',
    'DataValidationError',
    'StationarityTestError',
    'VisualizationError'
]
