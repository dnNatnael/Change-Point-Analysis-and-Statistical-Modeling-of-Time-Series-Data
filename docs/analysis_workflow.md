# Data Analysis Workflow for Brent Oil Price Change Point Analysis

## Overview
This document outlines the comprehensive workflow for analyzing Brent oil price data using change point detection and statistical modeling techniques. The objective is to identify structural breaks in price movements and understand their relationship with major geopolitical and economic events.

---

## Phase 1: Data Acquisition and Preprocessing

### 1.1 Data Loading
- Load Brent oil price historical data from CSV source
- Parse date columns and set appropriate datetime index
- Verify data completeness and date range coverage
- Handle any missing values through interpolation or forward-fill methods

### 1.2 Data Quality Assessment
- Check for gaps in time series continuity
- Identify outliers and anomalous price movements
- Validate price ranges against historical records
- Document any data quality issues and remediation steps

### 1.3 Data Transformation
- Convert prices to log-returns for volatility analysis
- Resample data to consistent frequency (daily/weekly) if needed
- Create derived features: rolling means, volatility measures
- Normalize data for certain modeling approaches

---

## Phase 2: Exploratory Data Analysis (EDA)

### 2.1 Trend Analysis
- Visualize long-term price evolution using line plots
- Decompose time series into trend, seasonal, and residual components
- Apply moving averages to identify long-term direction
- Detect major bull and bear market periods

### 2.2 Stationarity Testing
- Perform Augmented Dickey-Fuller (ADF) test
- Conduct KPSS test for trend stationarity
- Evaluate results to determine differencing requirements
- Document non-stationarity patterns and their implications

### 2.3 Volatility Analysis
- Calculate rolling standard deviation windows (30, 60, 90 days)
- Identify periods of high and low volatility clustering
- Apply ARCH/GARCH models if heteroscedasticity detected
- Visualize volatility regimes using heatmaps

### 2.4 Autocorrelation Analysis
- Generate ACF and PACF plots
- Identify seasonality patterns and cyclical behaviors
- Assess mean-reversion vs momentum characteristics

---

## Phase 3: Change Point Detection

### 3.1 Model Selection
- Evaluate CUSUM (Cumulative Sum) algorithms for mean shifts
- Consider Bayesian Change Point Detection for uncertainty quantification
- Apply PELT (Pruned Exact Linear Time) for optimal segmentation
- Select appropriate cost functions (L2, L1, or custom)

### 3.2 Model Implementation
- Configure penalty parameters using BIC/AIC criteria
- Run change point detection on price levels and returns
- Validate detected points against known major events
- Perform sensitivity analysis on penalty choices

### 3.3 Structural Break Validation
- Apply Chow test for known break dates
- Use Zivot-Andrews test for unit roots with breaks
- Cross-validate findings with regime-switching models

---

## Phase 4: Event Correlation Analysis

### 4.1 Event Data Integration
- Load compiled event dataset (CSV format)
- Align event dates with detected change points
- Create temporal proximity metrics (±30, ±60, ±90 days)

### 4.2 Correlation Assessment
- Statistical testing of temporal alignment
- Granger causality tests for predictive relationships
- Event study methodology implementation
- Effect size estimation for significant events

### 4.3 Causal Analysis Considerations
- Document correlation vs. causation distinctions
- Identify confounding variables
- Apply difference-in-differences where appropriate

---

## Phase 5: Model Evaluation and Validation

### 5.1 Performance Metrics
- Precision and recall for change point detection
- False positive rate assessment
- Backtesting against holdout periods
- Model stability across different time windows

### 5.2 Robustness Checks
- Bootstrap confidence intervals for change points
- Sensitivity to parameter choices
- Out-of-sample validation
- Alternative model comparison

---

## Phase 6: Insight Generation and Reporting

### 6.1 Pattern Synthesis
- Characterize identified regimes (pre/post change point)
- Quantify price impact magnitudes
- Develop event classification system

### 6.2 Visualization Dashboard
- Interactive time series with annotated change points
- Event timeline overlay plots
- Volatility regime heatmaps
- Statistical test result summaries

### 6.3 Stakeholder Communication
- Executive summary with key findings
- Technical appendix with methodology details
- Policy recommendations for risk management
- Predictive insights for future monitoring

---

## Code Implementation Reference

This workflow is implemented through the following code artifacts:

### Python Modules (`src/`)

| Module | Workflow Phases | Key Functions |
|--------|-----------------|---------------|
| `data_loader.py` | Phase 1 | `load_brent_data()`, `validate_data()`, `clean_data()`, `compute_log_returns()` |
| `time_series_analysis.py` | Phase 2 | `run_stationarity_tests()` (ADF, KPSS), `compute_volatility()`, `test_arch_effects()` |
| `visualization.py` | Phase 2, 6 | `plot_price_trend()`, `plot_volatility_analysis()`, `plot_stationarity_diagnostics()`, `plot_events_overlay()` |
| `main_analysis.py` | All Phases | Complete pipeline script executing full workflow |

### Jupyter Notebook (`notebooks/`)

**`01_time_series_analysis.ipynb`** - Interactive implementation of:
- Data loading with validation checks
- Stationarity testing (ADF, KPSS) with annotated outputs
- Log returns computation and statistical summary
- Volatility analysis with regime detection (Low/Medium/High)
- ARCH effects testing for volatility clustering
- 5 comprehensive visualizations saved to `outputs/`

### Event Dataset (`references/`)

**`geopolitical_events.csv`** - Structured dataset with 18 events:
- Event_Date, Event_Type, Event_Name, Description
- Expected_Impact (High/Moderate/Low Positive/Negative)
- Region classification

### Usage Example

```python
# Load and validate data
df = load_brent_data("data/raw/BrentOilPrices.csv")
validation = validate_data(df)

# Run stationarity tests
results = run_stationarity_tests(df['Price'], "Price Levels")
print(f"Classification: {results['consensus']['classification']}")

# Compute returns and volatility
df_returns = compute_log_returns(df)
df_vol = compute_volatility(df_returns)
df_regimes = detect_volatility_regimes(df_vol)

# Generate visualizations
plot_price_trend(df)
plot_volatility_analysis(df_regimes)
```

---

## Communication Channels

| Audience | Format | Channel | Frequency |
|----------|--------|---------|-----------|
| Executives | Summary slides | Email + presentation | Monthly |
| Analysts | Technical reports | Shared drive + GitHub | Weekly |
| Risk Management | Alerts dashboard | Real-time API | Continuous |
| External stakeholders | Blog posts / whitepapers | Company website | Quarterly |

---

## Key References for Methodology

1. **Killick & Eckley (2014)**: changepoint: An R Package for Changepoint Analysis - Foundation for PELT algorithm
2. **Bai & Perron (2003)**: Computation and analysis of multiple structural change models - Multiple breakpoint estimation
3. **Hamilton (2008)**: Oil and the Macroeconomy - Historical context for oil price shocks
4. **Gately (2014)**: The Demand for Oil Products - Understanding demand-side drivers

---

## Success Criteria

- Identify minimum 80% of visually apparent structural breaks
- Temporal alignment within 90 days for 60% of major events
- Documented causal pathways for top 5 price regime changes
- Reproducible analysis pipeline with version control
