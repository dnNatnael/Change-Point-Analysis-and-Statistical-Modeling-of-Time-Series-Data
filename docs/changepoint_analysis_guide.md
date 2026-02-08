# Bayesian Change Point Analysis - User Guide

## Quick Start Guide

This guide will help you get started with the Bayesian change point analysis for Brent oil prices.

## Table of Contents

1. [Installation](#installation)
2. [Running the Analysis](#running-the-analysis)
3. [Understanding the Output](#understanding-the-output)
4. [Customization Options](#customization-options)
5. [Troubleshooting](#troubleshooting)
6. [Examples](#examples)

---

## 1. Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Jupyter Notebook or JupyterLab

### Install Dependencies

```bash
# Navigate to project directory
cd /path/to/Change-Point-Analysis-and-Statistical-Modeling-of-Time-Series-Data

# Install required packages
pip install -r requirements.txt
```

### Key Dependencies

- `pymc>=5.0.0` - Bayesian modeling framework
- `arviz>=0.15.0` - Bayesian diagnostics and visualization
- `pandas>=1.5.0` - Data manipulation
- `numpy>=1.21.0` - Numerical computing
- `matplotlib>=3.5.0` - Plotting
- `seaborn>=0.11.0` - Statistical visualization

---

## 2. Running the Analysis

### Option 1: Jupyter Notebook (Recommended)

1. **Start Jupyter:**
   ```bash
   jupyter notebook
   ```

2. **Open the notebook:**
   - Navigate to `notebooks/02_bayesian_changepoint_analysis.ipynb`

3. **Run cells sequentially:**
   - Execute each cell in order
   - Wait for MCMC sampling to complete (may take 5-10 minutes)

### Option 2: Python Script

```python
from src.data_loader import load_brent_data, clean_data, compute_log_returns
from src.bayesian_changepoint import BayesianChangePointModel

# Load and prepare data
df = load_brent_data("data/raw/BrentOilPrices.csv")
df_clean = clean_data(df)
df_returns = compute_log_returns(df_clean)
returns = df_returns['Log_Returns'].dropna()

# Build and fit model
model = BayesianChangePointModel(returns, name="BrentOil")
model.build_model(model_type="mean_shift")
trace = model.sample(draws=2000, tune=1000, chains=4)

# Get results
tau_idx, tau_date = model.get_change_point_estimate()
impact = model.compute_impact()

print(f"Change point detected: {tau_date}")
print(f"Mean change: {impact['mu_change']}")
```

---

## 3. Understanding the Output

### Model Summary

The model summary table shows key statistics for each parameter:

```
           mean     sd  hdi_3%  hdi_97%  mcse_mean  mcse_sd  ess_bulk  ess_tail  r_hat
tau      1234.5   45.2  1150.0   1320.0       0.8      0.6    3200.0    3100.0   1.00
mu_before -0.001  0.002  -0.005   0.003       0.0      0.0    4500.0    4200.0   1.00
mu_after   0.002  0.002  -0.002   0.006       0.0      0.0    4300.0    4100.0   1.00
sigma      0.025  0.001   0.023   0.027       0.0      0.0    4800.0    4500.0   1.00
```

**Key Columns:**
- `mean`: Posterior mean (best point estimate)
- `sd`: Posterior standard deviation (uncertainty)
- `hdi_3%`, `hdi_97%`: 94% Highest Density Interval (credible interval)
- `ess_bulk`, `ess_tail`: Effective sample size (should be > 400)
- `r_hat`: Convergence diagnostic (should be < 1.01)

### Change Point Identification

**Output:**
```
Change Point: 2014-06-15
Probability mass: 0.85
95% Credible Interval: [2014-05-20, 2014-07-10]
```

**Interpretation:**
- Most likely change point is June 15, 2014
- 85% of posterior samples fall on this date (high certainty)
- 95% confident the change occurred between May 20 and July 10

### Impact Quantification

**Output:**
```
Mean Before: -0.0005 (-0.05%)
Mean After:   0.0015 (0.15%)
Change:       0.0020 (0.20%)
Percent Change: 400%
Cohen's d: 0.65 (medium effect)
```

**Interpretation:**
- Average daily log return increased from -0.05% to 0.15%
- This is a 0.20 percentage point increase
- Effect size is medium (Cohen's d = 0.65)
- Statistically and practically significant

### Probabilistic Statements

**Output:**
```
Probability mean increased: 97.5%
Probability mean decreased: 2.5%
95% CI for change: [0.0010, 0.0030]
```

**Interpretation:**
- Very high confidence (97.5%) that mean increased
- The increase is between 0.10% and 0.30% with 95% probability
- Change is unlikely to be zero (CI doesn't include 0)

---

## 4. Customization Options

### Model Types

**Mean Shift Only:**
```python
model.build_model(model_type="mean_shift")
```
- Assumes constant volatility
- Faster, simpler
- Good for detecting level shifts

**Mean and Variance Shift:**
```python
model.build_model(model_type="mean_variance_shift")
```
- Allows volatility to change
- More flexible
- Better for regime changes

### Sampling Parameters

**Quick Test (Fast, Less Accurate):**
```python
trace = model.sample(draws=500, tune=500, chains=2)
```

**Standard (Recommended):**
```python
trace = model.sample(draws=2000, tune=1000, chains=4)
```

**High Precision (Slow, More Accurate):**
```python
trace = model.sample(draws=5000, tune=2000, chains=4, target_accept=0.99)
```

### Multiple Change Points

**Detect 3 change points:**
```python
from src.bayesian_changepoint import detect_multiple_changepoints

models = detect_multiple_changepoints(
    returns,
    n_changepoints=3,
    model_type="mean_shift",
    draws=1500,
    tune=1000
)
```

### Custom Priors

For advanced users, modify priors in the source code:

```python
# In src/bayesian_changepoint.py, modify build_model():

# More informative prior (if you expect change around index 1000)
tau = pm.Normal('tau', mu=1000, sigma=100)

# Stronger prior on means (if you expect small changes)
mu_1 = pm.Normal('mu_before', mu=0, sigma=1)
mu_2 = pm.Normal('mu_after', mu=0, sigma=1)
```

---

## 5. Troubleshooting

### Issue: Convergence Warnings

**Symptoms:**
```
WARNING: R-hat values exceed 1.01
WARNING: Low ESS detected
```

**Solutions:**
1. Increase sampling:
   ```python
   trace = model.sample(draws=5000, tune=2000, chains=4)
   ```

2. Increase target acceptance:
   ```python
   trace = model.sample(target_accept=0.99)
   ```

3. Check for data issues (outliers, missing values)

### Issue: Slow Sampling

**Symptoms:**
- Sampling takes > 30 minutes
- Progress bar stuck

**Solutions:**
1. Reduce data size (analyze subset):
   ```python
   returns_subset = returns['2010':'2020']
   ```

2. Use fewer chains:
   ```python
   trace = model.sample(chains=2)
   ```

3. Use mean-shift model (faster than mean-variance):
   ```python
   model.build_model(model_type="mean_shift")
   ```

### Issue: Flat Posterior for τ

**Symptoms:**
- Posterior distribution of τ is uniform
- No clear peak

**Possible Causes:**
1. No change point in data
2. Change is too gradual
3. Insufficient data

**Solutions:**
1. Check if change point actually exists (visual inspection)
2. Try different time periods
3. Consider smooth transition models

### Issue: Memory Error

**Symptoms:**
```
MemoryError: Unable to allocate array
```

**Solutions:**
1. Reduce number of draws:
   ```python
   trace = model.sample(draws=1000)
   ```

2. Analyze data in chunks
3. Use a machine with more RAM

### Issue: Import Errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'pymc'
```

**Solutions:**
1. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. Check Python version (need 3.8+):
   ```bash
   python --version
   ```

3. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

---

## 6. Examples

### Example 1: Basic Single Change Point

```python
import pandas as pd
from src.data_loader import load_brent_data, clean_data, compute_log_returns
from src.bayesian_changepoint import BayesianChangePointModel
from src.changepoint_visualization import plot_data_with_changepoint

# Load data
df = load_brent_data("data/raw/BrentOilPrices.csv")
df_clean = clean_data(df)
df_returns = compute_log_returns(df_clean)
returns = df_returns['Log_Returns'].dropna()

# Fit model
model = BayesianChangePointModel(returns)
model.build_model(model_type="mean_shift")
trace = model.sample(draws=2000, tune=1000, chains=4)

# Check convergence
diagnostics = model.check_convergence()
if diagnostics['r_hat_ok'] and diagnostics['ess_ok']:
    print("✓ Model converged!")

# Get results
tau_idx, tau_date = model.get_change_point_estimate()
impact = model.compute_impact()

print(f"\nChange Point: {tau_date}")
print(f"Mean Change: {impact['mu_change']:.6f}")
print(f"Effect Size: {impact['cohens_d']:.4f}")

# Visualize
fig = plot_data_with_changepoint(returns, model)
plt.show()
```

### Example 2: Multiple Change Points with Events

```python
from src.data_loader import load_events_data
from src.bayesian_changepoint import detect_multiple_changepoints
from src.changepoint_visualization import (
    plot_multiple_changepoints,
    create_impact_summary_table
)

# Load data and events
df = load_brent_data("data/raw/BrentOilPrices.csv")
df_clean = clean_data(df)
df_returns = compute_log_returns(df_clean)
returns = df_returns['Log_Returns'].dropna()
events = load_events_data("references/geopolitical_events.csv")

# Detect multiple change points
models = detect_multiple_changepoints(
    returns,
    n_changepoints=3,
    draws=1500,
    tune=1000
)

# Create summary
summary = create_impact_summary_table(models, events=events)
print(summary)

# Visualize
fig = plot_multiple_changepoints(returns, models, events=events)
plt.show()
```

### Example 3: Comparing Model Types

```python
# Fit both model types
model_mean = BayesianChangePointModel(returns, name="MeanShift")
model_mean.build_model(model_type="mean_shift")
trace_mean = model_mean.sample(draws=2000, tune=1000, chains=4)

model_var = BayesianChangePointModel(returns, name="MeanVarShift")
model_var.build_model(model_type="mean_variance_shift")
trace_var = model_var.sample(draws=2000, tune=1000, chains=4)

# Compare using WAIC
import arviz as az
waic_mean = az.waic(trace_mean)
waic_var = az.waic(trace_var)

print(f"Mean-only model WAIC: {waic_mean.waic:.2f}")
print(f"Mean-Var model WAIC: {waic_var.waic:.2f}")

if waic_var.waic < waic_mean.waic:
    print("→ Mean-Variance model fits better")
else:
    print("→ Mean-only model is sufficient")
```

### Example 4: Sensitivity Analysis

```python
# Test different prior specifications
results = []

for sigma_prior in [1, 5, 10, 20]:
    model = BayesianChangePointModel(returns)
    # Modify prior in source code or create custom model
    model.build_model(model_type="mean_shift")
    trace = model.sample(draws=1500, tune=1000, chains=4)
    
    tau_idx, tau_date = model.get_change_point_estimate()
    impact = model.compute_impact()
    
    results.append({
        'prior_sigma': sigma_prior,
        'tau_date': tau_date,
        'mean_change': impact['mu_change']
    })

# Compare results
results_df = pd.DataFrame(results)
print(results_df)
```

---

## Additional Resources

### Documentation

- [Methodology Document](bayesian_changepoint_methodology.md) - Detailed theoretical background
- [API Reference](../src/bayesian_changepoint.py) - Function documentation
- [Visualization Guide](../src/changepoint_visualization.py) - Plotting functions

### External Resources

- [PyMC Documentation](https://www.pymc.io/)
- [ArviZ Documentation](https://arviz-devs.github.io/arviz/)
- [Bayesian Methods for Hackers](https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers)

### Getting Help

1. Check this guide and methodology document
2. Review example notebooks
3. Consult PyMC documentation
4. Check convergence diagnostics carefully
5. Visualize results to understand what's happening

---

## Best Practices

### Do's ✓

- Always check convergence diagnostics
- Plot trace plots and posteriors
- Report uncertainty (credible intervals)
- Validate with domain knowledge
- Use stationary data (returns, not prices)
- Start with simple models
- Document your analysis

### Don'ts ✗

- Don't ignore convergence warnings
- Don't over-interpret weak signals
- Don't forget to check assumptions
- Don't use raw prices (non-stationary)
- Don't fit too many change points
- Don't skip visual inspection
- Don't report only point estimates

---

**Last Updated**: 2024  
**Version**: 1.0  
**Maintainer**: Data Analysis Team
