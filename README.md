# Change-Point-Analysis-and-Statistical-Modeling-of-Time-Series-Data

## Project Overview

This project implements **change point detection** and **statistical modeling** techniques to analyze structural breaks in Brent oil price time series data. The objective is to identify periods of regime change in oil prices and correlate them with major geopolitical events, OPEC policy decisions, and economic shocks.

---

## Project Structure

```
Change-Point-Analysis-and-Statistical-Modeling-of-Time-Series-Data/
├── data/
│   ├── raw/                    # Original Brent oil price data (gitignored)
│   │   └── BrentOilPrices.csv
│   └── processed/              # Cleaned and transformed datasets
├── notebooks/                  # Jupyter notebooks for analysis
│   └── 01_time_series_analysis.ipynb  # Main analysis notebook (ADF, KPSS, volatility)
├── src/                        # Modular Python source code
│   ├── __init__.py            # Package initialization with exports
│   ├── data_loader.py         # Data loading and validation functions
│   ├── time_series_analysis.py # Statistical tests (ADF, KPSS, ARCH)
│   ├── visualization.py       # Plotting functions
│   └── main_analysis.py       # Complete analysis pipeline script
├── outputs/                    # Generated outputs (plots, results)
├── docs/                       # Project documentation
│   ├── analysis_workflow.md    # Complete analysis workflow (1-2 pages)
│   ├── assumptions_and_limitations.md  # Critical analysis constraints
│   └── model_and_data_understanding.md # Model theory and data properties
├── references/                 # Supporting reference data
│   └── geopolitical_events.csv # 18 key oil market events (1986-2022)
├── requirements.txt            # Python package dependencies
├── .gitignore                  # Data folder exclusion
└── README.md                   # This file
```

---

## Deliverables

### 1. Analysis Workflow Document
**Location:** `docs/analysis_workflow.md`

A comprehensive 1-2 page document outlining:
- 6-phase analysis workflow from data loading to insight generation
- Communication channels for stakeholder engagement
- Key references for methodology
- Success criteria and evaluation metrics

### 2. Geopolitical Events Dataset
**Location:** `references/geopolitical_events.csv`

Structured CSV containing **18 major oil market events** spanning 1986-2022:
- Event dates and types (OPEC Policy, Geopolitical, Financial, Natural Disaster)
- Event names and detailed descriptions
- Expected price impact (High/Moderate/Low Positive/Negative)
- Affected regions

**Key Events Include:**
- OPEC Price War Collapse (1986)
- Iraq Invasion of Kuwait (1990)
- Gulf War (1991)
- Asian Financial Crisis (1997)
- September 11 Attacks (2001)
- Hurricane Katrina (2005)
- Global Financial Crisis (2008)
- Arab Spring (2010-2011)
- OPEC Supply Glut Decision (2014)
- COVID-19 Oil Price Crash (2020)
- Russia-Ukraine War (2022)

### 3. Time Series Analysis Notebook
**Location:** `notebooks/01_time_series_analysis.ipynb`

Interactive Jupyter notebook implementing:
- Data loading and validation
- Stationarity testing (ADF, KPSS) with annotated results
- Log returns computation and analysis
- Volatility analysis with regime detection
- ARCH effects testing
- Comprehensive visualizations

### 4. Modular Python Source Code
**Location:** `src/`

Well-structured Python modules with error handling:
- `data_loader.py`: Data loading, validation, cleaning, and transformation
- `time_series_analysis.py`: ADF/KPSS tests, volatility computation, ARCH testing
- `visualization.py`: Trend plots, volatility charts, event overlays
- `main_analysis.py`: Complete analysis pipeline script

### 5. Assumptions and Limitations Documentation
**Location:** `docs/assumptions_and_limitations.md`

Critical documentation covering:
- Core assumptions about data quality, temporal independence, and model specification
- **Correlation vs. Causation discussion** - fundamental limitation of temporal analysis
- Methodological limitations of change point detection algorithms
- Scope limitations and appropriate/inappropriate uses
- Recommendations for stakeholders (risk managers, policy analysts, researchers)

### 6. Model and Data Understanding
**Location:** `docs/model_and_data_understanding.md`

Technical foundation document covering:
- **Time series properties**: Trend analysis, stationarity testing, volatility patterns
- **Change point models**: Purpose, application to oil prices, algorithm comparison
- **Expected outputs**: Detected dates, regime boundaries, parameter estimates
- **Key references**: Foundational papers and domain-specific applications

---

## Analysis Methodology

### Phase 1: Data Preprocessing
- Load historical Brent oil price data
- Quality assessment and missing value handling
- Data transformation (log-returns, volatility measures)

### Phase 2: Exploratory Data Analysis
- Trend decomposition
- Stationarity testing (ADF, KPSS)
- Volatility clustering analysis

### Phase 3: Change Point Detection
- Apply PELT (Pruned Exact Linear Time) algorithm for optimal segmentation
- Binary segmentation for comparison
- Bayesian methods for uncertainty quantification

### Phase 4: Event Correlation
- Align detected change points with compiled event dataset
- Statistical testing of temporal alignment
- Granger causality analysis

### Phase 5: Model Validation
- Bootstrap confidence intervals
- Sensitivity analysis
- Backtesting on holdout periods

### Phase 6: Reporting
- Interactive visualizations
- Executive summaries
- Technical appendices

---

## Key Algorithms

| Algorithm | Use Case |
|-----------|----------|
| **PELT** | Optimal change point detection with O(n) complexity |
| **CUSUM** | Online/real-time change detection |
| **Binary Segmentation** | Fast approximate detection for large datasets |
| **Bayesian Change Point** | Uncertainty quantification around change dates |

---

## Data Sources

- **Primary:** Historical Brent crude oil daily prices
- **Events:** Compiled from historical records of OPEC decisions, geopolitical events, and economic crises

---

## References

### Methodology
1. Killick, R., Fearnhead, P., & Eckley, I. A. (2012). "Optimal detection of changepoints with a linear computational cost." *Journal of the American Statistical Association*.
2. Bai, J., & Perron, P. (1998). "Estimating and testing linear models with multiple structural changes." *Econometrica*.

### Domain
3. Hamilton, J. D. (2008). "Oil and the macroeconomy."
4. Kilian, L. (2009). "Not all oil price shocks are alike." *American Economic Review*.

---

## Getting Started

### Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify the data file is present:**
   - Ensure `data/raw/BrentOilPrices.csv` exists
   - The data folder is gitignored but required for analysis

### Usage

#### Option 1: Jupyter Notebook (Recommended for Exploration)

Launch the main analysis notebook:
```bash
jupyter notebook notebooks/01_time_series_analysis.ipynb
```

This notebook provides:
- Interactive data exploration
- Step-by-step stationarity testing with annotated results
- Real-time visualization generation
- Export of processed data to `outputs/` folder

#### Option 2: Python Script (Command Line)

Run the complete analysis pipeline:
```bash
python src/main_analysis.py
```

This executes:
- Data loading and validation
- Stationarity tests (ADF, KPSS) with logged results
- Volatility analysis and regime detection
- Generation of 5 visualization plots in `outputs/`

#### Option 3: Import as Module

Use the source modules in your own scripts:
```python
from src import load_brent_data, run_stationarity_tests
from src import plot_price_trend, compute_volatility

# Load and analyze data
df = load_brent_data("data/raw/BrentOilPrices.csv")
results = run_stationarity_tests(df['Price'], "Price Levels")
print(results['consensus']['classification'])
```

### Quick Reference

- `docs/analysis_workflow.md` - Complete methodology
- `notebooks/01_time_series_analysis.ipynb` - Interactive analysis
- `src/main_analysis.py` - Command-line pipeline
- `references/geopolitical_events.csv` - Event dataset

---

## Communication Channels

| Stakeholder | Format | Frequency |
|-------------|--------|-----------|
| Executives | Summary slides | Monthly |
| Analysts | Technical reports | Weekly |
| Risk Management | Dashboard alerts | Real-time |
| External | Whitepapers | Quarterly |

---

## Important Notes

⚠️ **Critical Limitation:** This analysis identifies **temporal associations** between events and price changes. It does **NOT prove causation**. Always consider:
- Confounding variables (multiple simultaneous factors)
- Reverse causality (prices causing events)
- Selection bias (unknown events)

See `docs/assumptions_and_limitations.md` for comprehensive discussion.

---

## License

This project is for educational and research purposes.