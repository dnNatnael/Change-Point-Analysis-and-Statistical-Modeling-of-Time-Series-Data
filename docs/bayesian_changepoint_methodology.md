# Bayesian Change Point Detection Methodology

## Overview

This document describes the Bayesian change point detection methodology implemented for analyzing structural breaks in Brent oil price time series data.

## Table of Contents

1. [Introduction](#introduction)
2. [Theoretical Background](#theoretical-background)
3. [Model Specification](#model-specification)
4. [Implementation Details](#implementation-details)
5. [Interpretation Guidelines](#interpretation-guidelines)
6. [Validation and Diagnostics](#validation-and-diagnostics)
7. [Limitations and Assumptions](#limitations-and-assumptions)
8. [References](#references)

---

## 1. Introduction

### Objective

Apply Bayesian change point detection to identify and quantify structural breaks in Brent oil prices, associating these breaks with geopolitical events and market dynamics.

### Why Bayesian Methods?

Bayesian change point detection offers several advantages over classical methods:

- **Full Uncertainty Quantification**: Provides complete posterior distributions, not just point estimates
- **Probabilistic Statements**: Enables statements like "95% probability the change occurred between dates X and Y"
- **Flexible Modeling**: Easy to incorporate prior knowledge and extend to complex scenarios
- **Robust Inference**: Naturally handles uncertainty in all parameters simultaneously
- **Interpretable Results**: Posterior distributions directly answer questions of interest

---

## 2. Theoretical Background

### Change Point Problem

A change point is a time index τ where the statistical properties of a time series change. For a time series {y₁, y₂, ..., yₙ}, we want to identify τ such that:

- For t < τ: yₜ ~ F₁(θ₁)
- For t ≥ τ: yₜ ~ F₂(θ₂)

where F₁ and F₂ are probability distributions with parameters θ₁ and θ₂.

### Bayesian Framework

In the Bayesian framework, we treat τ and all parameters as random variables with prior distributions. We then use observed data to update these priors to posterior distributions via Bayes' theorem:

```
P(τ, θ | data) ∝ P(data | τ, θ) × P(τ) × P(θ)
```

Where:
- P(τ, θ | data) is the posterior distribution
- P(data | τ, θ) is the likelihood
- P(τ) and P(θ) are prior distributions

### MCMC Sampling

Since the posterior distribution is typically intractable analytically, we use Markov Chain Monte Carlo (MCMC) methods to draw samples from it. Specifically, we use the No-U-Turn Sampler (NUTS), an advanced variant of Hamiltonian Monte Carlo.

---

## 3. Model Specification

### Model 1: Mean Shift Model

The simplest change point model assumes only the mean changes:

**Priors:**
```
τ ~ DiscreteUniform(0, n-1)
μ₁ ~ Normal(0, 10)
μ₂ ~ Normal(0, 10)
σ ~ HalfNormal(10)
```

**Likelihood:**
```
yₜ ~ Normal(μ(t), σ)

where μ(t) = {
    μ₁  if t < τ
    μ₂  if t ≥ τ
}
```

**Interpretation:**
- τ: The change point (time index)
- μ₁: Mean before the change point
- μ₂: Mean after the change point
- σ: Standard deviation (constant across regimes)

### Model 2: Mean and Variance Shift Model

A more flexible model allows both mean and variance to change:

**Priors:**
```
τ ~ DiscreteUniform(0, n-1)
μ₁ ~ Normal(0, 10)
μ₂ ~ Normal(0, 10)
σ₁ ~ HalfNormal(10)
σ₂ ~ HalfNormal(10)
```

**Likelihood:**
```
yₜ ~ Normal(μ(t), σ(t))

where:
μ(t) = {μ₁ if t < τ, μ₂ if t ≥ τ}
σ(t) = {σ₁ if t < τ, σ₂ if t ≥ τ}
```

**Interpretation:**
- Captures both level shifts and volatility regime changes
- More flexible but requires more data for reliable estimation

### Prior Selection Rationale

**Change Point (τ):**
- DiscreteUniform(0, n-1): Non-informative prior giving equal probability to all possible change points
- Alternative: Could use informative prior if we have strong beliefs about timing

**Means (μ₁, μ₂):**
- Normal(0, 10): Weakly informative prior centered at zero
- For log returns, this is reasonable as they typically have small means
- Standard deviation of 10 allows for wide range of possible values

**Standard Deviations (σ, σ₁, σ₂):**
- HalfNormal(10): Weakly informative prior for positive values
- Appropriate for standard deviations which must be positive
- Allows for both low and high volatility regimes

---

## 4. Implementation Details

### Data Preparation

1. **Load Raw Prices**: Import Brent oil price data
2. **Clean Data**: Handle missing values using linear interpolation
3. **Compute Log Returns**: Transform to log returns for stationarity
   ```
   rₜ = ln(Pₜ / Pₜ₋₁)
   ```
4. **Remove NaN**: Drop first observation (no previous price)

### Model Building (PyMC)

```python
import pymc as pm

with pm.Model() as model:
    # Change point prior
    tau = pm.DiscreteUniform('tau', lower=0, upper=n-1)
    
    # Parameter priors
    mu_before = pm.Normal('mu_before', mu=0, sigma=10)
    mu_after = pm.Normal('mu_after', mu=0, sigma=10)
    sigma = pm.HalfNormal('sigma', sigma=10)
    
    # Switch function
    idx = np.arange(n)
    mu = pm.math.switch(tau >= idx, mu_before, mu_after)
    
    # Likelihood
    obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=data)
```

### MCMC Sampling Configuration

**Recommended Settings:**
- **Draws**: 2000 per chain (post-warmup samples)
- **Tune**: 1000 (warmup/burn-in samples)
- **Chains**: 4 (for convergence assessment)
- **Target Accept**: 0.95 (for discrete parameters)
- **Random Seed**: Set for reproducibility

**Computational Considerations:**
- Single change point: ~2-5 minutes
- Multiple change points: ~10-30 minutes (sequential fitting)
- Memory: ~500MB-1GB for typical datasets

### Multiple Change Points

For detecting multiple change points, we use a sequential approach:

1. Fit model to full data → detect CP₁
2. Split data at CP₁, fit to second segment → detect CP₂
3. Continue for desired number of change points

**Limitations of Sequential Approach:**
- Assumes change points are well-separated
- Earlier detections influence later ones
- Alternative: Simultaneous detection (more complex, computationally intensive)

---

## 5. Interpretation Guidelines

### Posterior Distribution of τ

**Sharp Peak:**
- High certainty about change point location
- Strong evidence for structural break
- Narrow credible interval

**Broad Distribution:**
- Uncertainty about exact timing
- Gradual transition or weak signal
- Wide credible interval

**Multiple Peaks:**
- Possible multiple change points
- Model uncertainty
- Consider multiple change point model

### Parameter Changes

**Mean Change (μ₂ - μ₁):**
- Positive: Increase in average returns (upward shift)
- Negative: Decrease in average returns (downward shift)
- Magnitude: Size of the shift

**Credible Intervals:**
- 95% CI not containing zero: Strong evidence for change
- 95% CI containing zero: Weak evidence, possibly no change

**Effect Size (Cohen's d):**
```
d = (μ₂ - μ₁) / σ_pooled
```

Interpretation:
- |d| < 0.2: Negligible effect
- 0.2 ≤ |d| < 0.5: Small effect
- 0.5 ≤ |d| < 0.8: Medium effect
- |d| ≥ 0.8: Large effect

### Probabilistic Statements

From posterior samples, we can make statements like:

- "There is a 95% probability the change point occurred between [date1] and [date2]"
- "The probability that the mean increased is 98%"
- "The expected change in mean is X% with 95% CI [Y%, Z%]"

---

## 6. Validation and Diagnostics

### Convergence Diagnostics

**R-hat (Gelman-Rubin Statistic):**
- Measures convergence across chains
- Target: R-hat < 1.01 (ideally < 1.001)
- R-hat > 1.01: Chains haven't converged, run more samples

**Effective Sample Size (ESS):**
- Accounts for autocorrelation in samples
- Target: ESS > 400 (bulk and tail)
- Low ESS: High autocorrelation, need more samples

**Trace Plots:**
- Visual inspection of chain behavior
- Good: Chains mix well, no trends, stable distribution
- Bad: Chains stuck, trending, not mixing

**Energy Plot:**
- Checks for bias in NUTS sampler
- Good: Distributions overlap well
- Bad: Significant separation indicates problems

### Model Comparison

**WAIC (Widely Applicable Information Criterion):**
- Lower is better
- Balances fit and complexity
- Use for comparing different model specifications

**LOO (Leave-One-Out Cross-Validation):**
- Estimates out-of-sample predictive performance
- More robust than WAIC
- Identifies influential observations

### Sensitivity Analysis

Test robustness to:
1. **Prior Specifications**: Try different prior parameters
2. **Data Subsets**: Analyze different time periods
3. **Outliers**: Check influence of extreme observations
4. **Model Specification**: Compare mean-only vs mean-variance models

---

## 7. Limitations and Assumptions

### Assumptions

1. **Single Change Point**: Basic model assumes only one structural break
   - Reality: Multiple breaks likely in long time series
   - Solution: Use multiple change point detection

2. **Instantaneous Change**: Model assumes abrupt transition
   - Reality: Changes may be gradual
   - Solution: Consider smooth transition models

3. **Independence**: Assumes observations are independent given regime
   - Reality: Time series often have autocorrelation
   - Solution: Model residual autocorrelation explicitly

4. **Normality**: Assumes normal distribution for returns
   - Reality: Financial returns have fat tails
   - Solution: Use Student-t or other heavy-tailed distributions

5. **Known Number of Change Points**: Must specify how many to detect
   - Reality: Unknown number of breaks
   - Solution: Use model selection criteria or reversible-jump MCMC

### Limitations

1. **Computational Cost**: MCMC can be slow for large datasets
2. **Sequential Detection**: Multiple change points detected sequentially, not simultaneously
3. **Discrete τ**: Change point must occur at observed time point
4. **No Covariates**: Basic model doesn't include external variables
5. **Retrospective**: Detects past change points, not real-time detection

### When to Use This Method

**Appropriate:**
- Historical analysis of structural breaks
- Sufficient data (n > 100 observations)
- Interest in uncertainty quantification
- Need for probabilistic statements
- Comparing multiple model specifications

**Not Appropriate:**
- Real-time detection (too slow)
- Very short time series (n < 50)
- When only point estimates needed
- Highly complex models (computational limits)

---

## 8. References

### Key Papers

1. **Bayesian Change Point Detection:**
   - Barry, D., & Hartigan, J. A. (1993). "A Bayesian analysis for change point problems." Journal of the American Statistical Association, 88(421), 309-319.

2. **MCMC Methods:**
   - Hoffman, M. D., & Gelman, A. (2014). "The No-U-Turn sampler: adaptively setting path lengths in Hamiltonian Monte Carlo." Journal of Machine Learning Research, 15(1), 1593-1623.

3. **Oil Price Analysis:**
   - Hamilton, J. D. (2009). "Causes and Consequences of the Oil Shock of 2007-08." Brookings Papers on Economic Activity, 2009(1), 215-261.

### Software Documentation

- **PyMC**: https://www.pymc.io/
- **ArviZ**: https://arviz-devs.github.io/arviz/
- **Bayesian Methods for Hackers**: https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers

### Related Methods

- **Ruptures**: Python library for offline change point detection
- **PELT**: Pruned Exact Linear Time algorithm
- **Binary Segmentation**: Recursive splitting approach
- **Hidden Markov Models**: For regime-switching models
- **Structural Break Tests**: Chow test, CUSUM, Bai-Perron

---

## Appendix: Practical Tips

### Improving Convergence

1. **Increase Samples**: More draws and longer tuning
2. **Reparameterization**: Transform parameters for better geometry
3. **Stronger Priors**: More informative priors can help
4. **Data Scaling**: Standardize data to improve sampler efficiency
5. **Initial Values**: Provide good starting points

### Interpreting Results

1. **Always Check Diagnostics**: Don't trust results without convergence
2. **Plot Everything**: Visual inspection is crucial
3. **Report Uncertainty**: Include credible intervals, not just point estimates
4. **Context Matters**: Interpret in light of domain knowledge
5. **Validate**: Compare with alternative methods and expert judgment

### Common Pitfalls

1. **Ignoring Convergence Warnings**: Always address R-hat and ESS issues
2. **Over-interpreting Weak Signals**: Not all peaks in posterior are meaningful
3. **Forgetting Uncertainty**: Point estimates alone are misleading
4. **Wrong Data Transformation**: Use stationary series (returns, not prices)
5. **Too Many Change Points**: Overfitting with sequential detection

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Authors**: Data Analysis Team
