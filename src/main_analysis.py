"""
Brent Oil Price Analysis - Main Script
=====================================
Comprehensive analysis pipeline for Brent oil price data including:
- Data loading and validation
- Time series analysis (ADF, KPSS, returns)
- Volatility analysis
- Visualization generation
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
from pathlib import Path

# Import custom modules
from src.data_loader import (
    load_brent_data, 
    validate_data, 
    clean_data, 
    compute_log_returns,
    load_events_data
)
from src.time_series_analysis import (
    run_stationarity_tests,
    compute_volatility,
    detect_volatility_regimes,
    compute_rolling_statistics,
    test_arch_effects
)
from src.visualization import (
    plot_price_trend,
    plot_returns_distribution,
    plot_volatility_analysis,
    plot_stationarity_diagnostics,
    plot_events_overlay
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
DATA_PATH = "data/raw/BrentOilPrices.csv"
EVENTS_PATH = "references/geopolitical_events.csv"
OUTPUT_DIR = "outputs"


def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def run_full_analysis():
    """
    Execute the complete analysis pipeline.
    
    Returns
    -------
    dict
        Dictionary containing all analysis results.
    """
    logger.info("=" * 60)
    logger.info("BRENT OIL PRICE - TIME SERIES ANALYSIS")
    logger.info("=" * 60)
    
    ensure_output_dir()
    results = {}
    
    # =====================================================================
    # PHASE 1: DATA LOADING AND VALIDATION
    # =====================================================================
    logger.info("\n" + "=" * 60)
    logger.info("PHASE 1: DATA LOADING AND VALIDATION")
    logger.info("=" * 60)
    
    try:
        # Load price data
        df_raw = load_brent_data(DATA_PATH)
        logger.info(f"Loaded {len(df_raw)} price records")
        
        # Validate data quality
        validation_results = validate_data(df_raw)
        results['validation'] = validation_results
        
        if not validation_results['is_valid']:
            logger.warning("Data validation issues detected. Attempting to clean...")
        
        # Clean data
        df_clean = clean_data(df_raw, fill_method='linear')
        
        # Load events data
        df_events = load_events_data(EVENTS_PATH)
        results['events_count'] = len(df_events)
        
    except Exception as e:
        logger.error(f"Phase 1 failed: {e}")
        raise
    
    # =====================================================================
    # PHASE 2: TIME SERIES ANALYSIS - STATIONARITY TESTS
    # =====================================================================
    logger.info("\n" + "=" * 60)
    logger.info("PHASE 2: STATIONARITY TESTING")
    logger.info("=" * 60)
    
    try:
        # Test 1: Price levels
        logger.info("\n--- Testing Price Levels ---")
        price_stationarity = run_stationarity_tests(df_clean['Price'], "Price Levels")
        results['price_stationarity'] = price_stationarity
        
        # Log results
        adf = price_stationarity['adf']
        kpss = price_stationarity['kpss']
        logger.info(f"  ADF Test: statistic={adf['test_statistic']:.4f}, p-value={adf['p_value']:.4f}")
        logger.info(f"    Result: {adf['interpretation']} - {adf['conclusion']}")
        logger.info(f"  KPSS Test: statistic={kpss['test_statistic']:.4f}, p-value={kpss['p_value']:.4f}")
        logger.info(f"    Result: {kpss['interpretation']} - {kpss['conclusion']}")
        logger.info(f"  Consensus: {price_stationarity['consensus']['classification']}")
        logger.info(f"  Recommendation: {price_stationarity['consensus']['recommendation']}")
        
        # Compute returns
        df_returns = compute_log_returns(df_clean)
        
        # Test 2: Log returns
        logger.info("\n--- Testing Log Returns ---")
        returns_stationarity = run_stationarity_tests(
            df_returns['Log_Returns'].dropna(), 
            "Log Returns"
        )
        results['returns_stationarity'] = returns_stationarity
        
        adf_r = returns_stationarity['adf']
        kpss_r = returns_stationarity['kpss']
        logger.info(f"  ADF Test: statistic={adf_r['test_statistic']:.4f}, p-value={adf_r['p_value']:.4f}")
        logger.info(f"    Result: {adf_r['interpretation']} - {adf_r['conclusion']}")
        logger.info(f"  KPSS Test: statistic={kpss_r['test_statistic']:.4f}, p-value={kpss_r['p_value']:.4f}")
        logger.info(f"    Result: {kpss_r['interpretation']} - {kpss_r['conclusion']}")
        logger.info(f"  Consensus: {returns_stationarity['consensus']['classification']}")
        
    except Exception as e:
        logger.error(f"Phase 2 failed: {e}")
        raise
    
    # =====================================================================
    # PHASE 3: VOLATILITY ANALYSIS
    # =====================================================================
    logger.info("\n" + "=" * 60)
    logger.info("PHASE 3: VOLATILITY ANALYSIS")
    logger.info("=" * 60)
    
    try:
        # Compute volatility measures
        df_vol = compute_volatility(df_returns, windows=[30, 60, 90])
        
        # Detect volatility regimes
        df_regimes = detect_volatility_regimes(df_vol, method='quantile')
        results['volatility_regimes'] = df_regimes['Volatility_Regime'].value_counts().to_dict()
        
        logger.info("\n--- Volatility Regime Distribution ---")
        for regime, count in df_regimes['Volatility_Regime'].value_counts().items():
            pct = count / len(df_regimes) * 100
            logger.info(f"  {regime}: {count} days ({pct:.1f}%)")
        
        # Test for ARCH effects
        logger.info("\n--- ARCH Effects Test ---")
        arch_results = test_arch_effects(df_returns['Log_Returns'].dropna())
        results['arch_test'] = arch_results
        
        if 'error' not in arch_results:
            logger.info(f"  LM Statistic: {arch_results['lm_statistic']:.4f}")
            logger.info(f"  p-value: {arch_results['lm_pvalue']:.4f}")
            logger.info(f"  Result: {arch_results['interpretation']}")
        
    except Exception as e:
        logger.error(f"Phase 3 failed: {e}")
        raise
    
    # =====================================================================
    # PHASE 4: ROLLING STATISTICS
    # =====================================================================
    logger.info("\n" + "=" * 60)
    logger.info("PHASE 4: ROLLING STATISTICS")
    logger.info("=" * 60)
    
    try:
        df_rolling = compute_rolling_statistics(df_regimes)
        
        # Summary statistics
        logger.info("\n--- Price Statistics ---")
        logger.info(f"  Mean: ${df_clean['Price'].mean():.2f}")
        logger.info(f"  Std Dev: ${df_clean['Price'].std():.2f}")
        logger.info(f"  Min: ${df_clean['Price'].min():.2f}")
        logger.info(f"  Max: ${df_clean['Price'].max():.2f}")
        
        logger.info("\n--- Returns Statistics ---")
        returns_clean = df_returns['Log_Returns'].dropna()
        logger.info(f"  Mean: {returns_clean.mean()*100:.4f}%")
        logger.info(f"  Std Dev (daily): {returns_clean.std()*100:.4f}%")
        logger.info(f"  Annualized Vol: {returns_clean.std() * np.sqrt(252) * 100:.2f}%")
        logger.info(f"  Skewness: {returns_clean.skew():.4f}")
        logger.info(f"  Kurtosis: {returns_clean.kurtosis():.4f}")
        
    except Exception as e:
        logger.error(f"Phase 4 failed: {e}")
        raise
    
    # =====================================================================
    # PHASE 5: VISUALIZATION
    # =====================================================================
    logger.info("\n" + "=" * 60)
    logger.info("PHASE 5: GENERATING VISUALIZATIONS")
    logger.info("=" * 60)
    
    try:
        # Plot 1: Price trend
        logger.info("  Creating price trend plot...")
        fig1 = plot_price_trend(
            df_rolling, 
            save_path=f"{OUTPUT_DIR}/01_price_trend.png"
        )
        plt.close(fig1)
        
        # Plot 2: Returns distribution
        logger.info("  Creating returns distribution plot...")
        fig2 = plot_returns_distribution(
            df_returns,
            save_path=f"{OUTPUT_DIR}/02_returns_distribution.png"
        )
        plt.close(fig2)
        
        # Plot 3: Volatility analysis
        logger.info("  Creating volatility analysis plot...")
        fig3 = plot_volatility_analysis(
            df_regimes,
            save_path=f"{OUTPUT_DIR}/03_volatility_analysis.png"
        )
        plt.close(fig3)
        
        # Plot 4: Stationarity diagnostics
        logger.info("  Creating stationarity diagnostics plot...")
        fig4 = plot_stationarity_diagnostics(
            df_returns,
            save_path=f"{OUTPUT_DIR}/04_stationarity_diagnostics.png"
        )
        plt.close(fig4)
        
        # Plot 5: Events overlay
        logger.info("  Creating events overlay plot...")
        fig5 = plot_events_overlay(
            df_clean,
            df_events,
            save_path=f"{OUTPUT_DIR}/05_events_overlay.png"
        )
        plt.close(fig5)
        
        logger.info(f"  All plots saved to {OUTPUT_DIR}/")
        
    except Exception as e:
        logger.error(f"Phase 5 failed: {e}")
        raise
    
    # =====================================================================
    # SUMMARY
    # =====================================================================
    logger.info("\n" + "=" * 60)
    logger.info("ANALYSIS COMPLETE - SUMMARY")
    logger.info("=" * 60)
    
    logger.info(f"\nData Coverage:")
    logger.info(f"  Period: {df_clean.index.min().strftime('%Y-%m-%d')} to {df_clean.index.max().strftime('%Y-%m-%d')}")
    logger.info(f"  Total observations: {len(df_clean)}")
    logger.info(f"  Events analyzed: {results['events_count']}")
    
    logger.info(f"\nKey Findings:")
    logger.info(f"  Price stationarity: {price_stationarity['consensus']['classification']}")
    logger.info(f"  Returns stationarity: {returns_stationarity['consensus']['classification']}")
    if 'arch_test' in results and 'interpretation' in results['arch_test']:
        logger.info(f"  Volatility clustering: {results['arch_test']['interpretation']}")
    
    logger.info(f"\nOutput Files:")
    logger.info(f"  Plots saved in: {OUTPUT_DIR}/")
    
    return results


if __name__ == "__main__":
    try:
        results = run_full_analysis()
        logger.info("\n" + "=" * 60)
        logger.info("SCRIPT COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
    except Exception as e:
        logger.error(f"\nSCRIPT FAILED: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)
