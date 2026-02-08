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
│   ├── 01_time_series_analysis.ipynb      # Initial EDA and stationarity tests
│   └── 02_bayesian_changepoint_analysis.ipynb  # ⭐ Bayesian change point detection
├── src/                        # Modular Python source code
│   ├── __init__.py            # Package initialization with exports
│   ├── data_loader.py         # Data loading and validation functions
│   ├── time_series_analysis.py # Statistical tests (ADF, KPSS, ARCH)
│   ├── visualization.py       # Plotting functions
│   ├── main_analysis.py       # Complete analysis pipeline script
│   ├── bayesian_changepoint.py         # ⭐ Bayesian change point models
│   └── changepoint_visualization.py    # ⭐ Change point visualizations
├── results/                    # ⭐ Generated outputs (model traces, summaries)
├── docs/                       # Project documentation
│   ├── analysis_workflow.md    # Complete analysis workflow (1-2 pages)
│   ├── assumptions_and_limitations.md  # Critical analysis constraints
│   ├── model_and_data_understanding.md # Model theory and data properties
│   ├── bayesian_changepoint_methodology.md  # ⭐ Bayesian methodology
│   ├── changepoint_analysis_guide.md        # ⭐ User guide
│   └── project_deliverables_summary.md      # ⭐ Deliverables checklist
├── references/                 # Supporting reference data
│   └── geopolitical_events.csv # ⭐ 45 key oil market events (1990-2024)
├── requirements.txt            # Python package dependencies (⭐ updated with PyMC)
├── .gitignore                  # Data folder exclusion 
└── README.md                   # This file
```

⭐ = New files for Bayesian change point analysis

---

## Deliverables

### 1. Bayesian Change Point Analysis ⭐ NEW
**Location:** `notebooks/02_bayesian_changepoint_analysis.ipynb`

Comprehensive Bayesian change point detection implementation:
- PyMC-based Bayesian models with MCMC sampling
- Mean shift and mean-variance shift models
- Convergence diagnostics (R-hat, ESS, trace plots)
- Posterior distributions with credible intervals
- Quantitative impact analysis with effect sizes
- Event association and hypothesis formulation
- Multiple change point detection
- Complete documentation and interpretation

**Supporting Files:**
- [`src/bayesian_changepoint.py`](src/bayesian_changepoint.py) - Core Bayesian models
- [`src/changepoint_visualization.py`](src/changepoint_visualization.py) - Specialized visualizations
- [`docs/bayesian_changepoint_methodology.md`](docs/bayesian_changepoint_methodology.md) - Theoretical background
- [`docs/changepoint_analysis_guide.md`](docs/changepoint_analysis_guide.md) - User guide
- [`CHANGEPOINT_README.md`](CHANGEPOINT_README.md) - Quick reference

### 2. Analysis Workflow Document
**Location:** `docs/analysis_workflow.md`

A comprehensive 1-2 page document outlining:
- 6-phase analysis workflow from data loading to insight generation
- Communication channels for stakeholder engagement
- Key references for methodology
- Success criteria and evaluation metrics

### 3. Geopolitical Events Dataset
**Location:** `references/geopolitical_events.csv`

Structured CSV containing **45 major oil market events** spanning 1990-2024:
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
- Israel-Hamas War (2023)
- Red Sea Tensions (2024)

### 4. Time Series Analysis Notebook
**Location:** `notebooks/01_time_series_analysis.ipynb`

Interactive Jupyter notebook implementing:
- Data loading and validation
- Stationarity testing (ADF, KPSS) with annotated results
- Log returns computation and analysis
- Volatility analysis with regime detection
- ARCH effects testing
- Comprehensive visualizations

### 5. Modular Python Source Code
**Location:** `src/`

Well-structured Python modules with error handling:
- `data_loader.py`: Data loading, validation, cleaning, and transformation
- `time_series_analysis.py`: ADF/KPSS tests, volatility computation, ARCH testing
- `visualization.py`: Trend plots, volatility charts, event overlays
- `main_analysis.py`: Complete analysis pipeline script
- `bayesian_changepoint.py`: ⭐ Bayesian change point models with PyMC
- `changepoint_visualization.py`: ⭐ Specialized change point visualizations

### 6. Assumptions and Limitations Documentation
**Location:** `docs/assumptions_and_limitations.md`

Critical documentation covering:
- Core assumptions about data quality, temporal independence, and model specification
- **Correlation vs. Causation discussion** - fundamental limitation of temporal analysis
- Methodological limitations of change point detection algorithms
- Scope limitations and appropriate/inappropriate uses
- Recommendations for stakeholders (risk managers, policy analysts, researchers)

### 7. Model and Data Understanding
**Location:** `docs/model_and_data_understanding.md`

Technical foundation document covering:
- **Time series properties**: Trend analysis, stationarity testing, volatility patterns
- **Change point models**: Purpose, application to oil prices, algorithm comparison
- **Expected outputs**: Detected dates, regime boundaries, parameter estimates
- **Key references**: Foundational papers and domain-specific applications

### 8. Bayesian Change Point Methodology ⭐ NEW
**Location:** `docs/bayesian_changepoint_methodology.md`

Comprehensive theoretical documentation:
- Bayesian framework and MCMC sampling
- Model specifications (mean shift, mean-variance shift)
- Prior selection rationale
- Implementation details with PyMC
- Interpretation guidelines
- Convergence diagnostics
- Limitations and assumptions
- Academic references

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
- ⭐ **Bayesian methods with PyMC** for full uncertainty quantification
  - Mean shift models
  - Mean-variance shift models
  - MCMC sampling with NUTS algorithm
  - Convergence diagnostics (R-hat, ESS)
  - Posterior distributions and credible intervals

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

| Algorithm | Use Case | Implementation |
|-----------|----------|----------------|
| **PELT** | Optimal change point detection with O(n) complexity | Planned |
| **CUSUM** | Online/real-time change detection | Planned |
| **Binary Segmentation** | Fast approximate detection for large datasets | Planned |
| **⭐ Bayesian Change Point (PyMC)** | Full uncertainty quantification with posterior distributions | ✓ Implemented |

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

**For Initial Time Series Analysis:**
```bash
jupyter notebook notebooks/01_time_series_analysis.ipynb
```

This notebook provides:
- Interactive data exploration
- Step-by-step stationarity testing with annotated results
- Real-time visualization generation
- Export of processed data to `outputs/` folder

**⭐ For Bayesian Change Point Analysis:**
```bash
jupyter notebook notebooks/02_bayesian_changepoint_analysis.ipynb
```

This notebook provides:
- Complete Bayesian change point detection
- MCMC sampling with PyMC
- Convergence diagnostics and validation
- Posterior distributions and credible intervals
- Quantitative impact analysis
- Event association and interpretation
- Multiple change point detection

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

**⭐ For Bayesian Change Point Detection:**
```python
from src.data_loader import load_brent_data, clean_data, compute_log_returns
from src.bayesian_changepoint import BayesianChangePointModel

# Load and prepare data
df = load_brent_data("data/raw/BrentOilPrices.csv")
df_clean = clean_data(df)
df_returns = compute_log_returns(df_clean)
returns = df_returns['Log_Returns'].dropna()

# Build and fit Bayesian model
model = BayesianChangePointModel(returns)
model.build_model(model_type="mean_shift")
trace = model.sample(draws=2000, tune=1000, chains=4)

# Get results
tau_idx, tau_date = model.get_change_point_estimate()
impact = model.compute_impact()

print(f"Change point: {tau_date}")
print(f"Mean change: {impact['mu_change']:.6f}")
print(f"Effect size: {impact['cohens_d']:.4f}")
```

### Quick Reference

**Time Series Analysis:**
- `docs/analysis_workflow.md` - Complete methodology
- `notebooks/01_time_series_analysis.ipynb` - Interactive analysis
- `src/main_analysis.py` - Command-line pipeline

**⭐ Bayesian Change Point Analysis:**
- `CHANGEPOINT_README.md` - Quick start guide
- `notebooks/02_bayesian_changepoint_analysis.ipynb` - Full Bayesian analysis
- `docs/bayesian_changepoint_methodology.md` - Theoretical background
- `docs/changepoint_analysis_guide.md` - User guide

**Data:**
- `references/geopolitical_events.csv` - Event dataset (45 events, 1990-2024)

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