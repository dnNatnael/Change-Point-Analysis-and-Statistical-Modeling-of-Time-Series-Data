# Understanding the Model and Data

## 1. Time Series Properties of Brent Oil Prices

### 1.1 Trend Analysis
Brent oil prices exhibit distinct trend patterns over the historical period (1987-present):

**Key Trend Characteristics:**
- **Long-term upward drift**: Prices show an overall increasing trend from ~$20/bbl (1987) to recent averages around $60-80/bbl, punctuated by sharp reversals
- **Super-cycle patterns**: Multi-year bull and bear markets driven by supply-demand imbalances
- **Non-linear growth**: Prices do not follow simple linear trends; exponential growth phases alternate with crashes
- **Persistence**: Once a trend establishes, it typically continues for months to years before reversing

**Implications for Modeling:**
- Raw prices are non-stationary and require differencing or transformation
- Trend-stationary models must account for structural shifts in the trend component
- Any valid model must incorporate regime-switching capabilities to capture the non-linear dynamics

### 1.2 Stationarity Testing
**Expected Findings:**
- **Price levels**: Will fail ADF (Augmented Dickey-Fuller) test; unit root present (non-stationary)
- **First differences (returns)**: Expected to be stationary, validating use of return-based models
- **KPSS test**: Likely to reject trend stationarity due to multiple structural breaks
- **Volatility**: GARCH effects expected; conditional heteroscedasticity requires specialized handling

**Modeling Choices Informed:**
- Standard ARIMA models insufficient; require structural break accommodation
- Cointegration analysis inappropriate without knowing break dates
- Change point detection provides preliminary regime identification before formal modeling

### 1.3 Volatility Patterns
**Stylized Facts for Brent Oil:**
- **Volatility clustering**: High volatility periods cluster around geopolitical crises
- **Leverage effects**: Price declines associated with higher subsequent volatility than equivalent rises
- **Regime-dependent variance**: Different volatility levels in "crisis" vs "stable" periods
- **News impact**: Exogenous shocks create sustained volatility elevation lasting weeks to months

**Prevalent High-Volatility Periods:**
1. Gulf War era (1990-1991)
2. Asian Financial Crisis and recovery (1997-1998)
3. 2008 Financial Crisis (July 2008 - March 2009)
4. Arab Spring and Libyan crisis (2011)
5. 2014-2016 Oil Glut period
6. COVID-19 pandemic (2020)
7. Russia-Ukraine conflict (2022-present)

---

## 2. Change Point Models: Purpose and Application

### 2.1 What Are Change Point Models?
Change point models are statistical methods designed to identify points in a time series where the underlying data-generating process undergoes a structural shift. These shifts can affect:
- **Mean level**: Sudden jumps or drops in average price
- **Variance**: Changes in volatility regime
- **Trend**: Alterations in the rate of price change
- **Distribution**: Changes in the entire probability distribution

### 2.2 Why Change Point Models for Oil Prices?
Oil markets are subject to **regime changes** driven by:
- **Supply shocks**: OPEC policy shifts, production disruptions
- **Demand cycles**: Global recessions, emerging market growth phases
- **Financialization**: Commodity index trading, speculative flows
- **Technological shifts**: Shale revolution, renewable substitution

Standard time series models (ARIMA, GARCH) assume parameter stability across the entire series. Oil prices violate this assumption, making change point detection essential for:
1. **Accurate forecasting**: Models trained on one regime fail in others
2. **Risk management**: Volatility and tail risk differ across regimes
3. **Event attribution**: Correlating detected breaks with known events
4. **Trading strategies**: Momentum vs mean-reversion strategies perform differently in different regimes

### 2.3 Algorithms Under Consideration

| Algorithm | Approach | Best For | Limitation |
|-----------|----------|----------|------------|
| **PELT (Pruned Exact Linear Time)** | Dynamic programming optimization | Large datasets, exact solution | Assumes known number of changes or penalty |
| **Binary Segmentation** | Greedy recursive splitting | Speed, detection of large changes | Approximate solution, local optima |
| **CUSUM** | Cumulative sum deviations | Online/real-time detection | Requires threshold tuning |
| **Bayesian Change Point** | Posterior distribution over change points | Uncertainty quantification | Computationally expensive |
| **Wild Binary Segmentation** | Random interval sampling | Detecting frequent changes | Multiple tuning parameters |

---

## 3. Expected Outputs and Limitations

### 3.1 Expected Outputs of Change Point Analysis

**Primary Outputs:**
1. **Change Point Dates**: List of detected dates where structural shifts occur
2. **Regime Boundaries**: Segmentation of time series into distinct periods
3. **Parameter Estimates**: Within-regime means, variances, trend slopes
4. **Confidence Intervals**: Uncertainty bounds around detected change dates
5. **Event Alignment Matrix**: Table mapping detected points to known events

**Secondary Outputs:**
- **Regime duration statistics**: Mean/median time between breaks
- **Volatility regime classification**: "High" vs "Low" volatility periods
- **Impact magnitude estimates**: Price change percentage around breaks
- **Visualization**: Annotated time series with marked change points

### 3.2 Example Output Format
```
Detected Change Points: 8
Date: 1990-09-01 | Type: Mean + Variance | Aligned Event: Gulf War (14 days offset)
Date: 1997-12-01 | Type: Trend | Aligned Event: Asian Financial Crisis (152 days offset)
Date: 2001-10-01 | Type: Variance | Aligned Event: 9/11 (20 days offset)
...
```

### 3.3 Critical Limitations

**Statistical Limitations:**
- **False positive rate**: Even with optimal penalty selection, expect 5-15% false detections
- **Detection delay**: Some methods lag behind actual change by days/weeks
- **Boundary effects**: Reduced sensitivity at series start and end
- **Parameter instability**: Inferred regime parameters have wide confidence intervals

**Interpretive Limitations:**
- **Multiple change points**: Adjacent detected points may reflect single complex event
- **Gradual transitions**: Models assume abrupt changes; gradual regime shifts poorly characterized
- **Missing events**: Not all change points align with documented events
- **Confounding**: Detected point may reflect endogenous market dynamics, not external events

**Operational Limitations:**
- **Computational constraints**: Exact optimization (PELT) may be slow for 30+ years of daily data
- **Storage requirements**: Full posterior distributions (Bayesian) require significant memory
- **Reproducibility**: Randomized methods (WBS) require seed setting for consistency

---

## 4. Key References for Implementation

### Foundational Papers
1. **Killick, R., Fearnhead, P., & Eckley, I. A. (2012).** "Optimal detection of changepoints with a linear computational cost." *Journal of the American Statistical Association*, 107(500), 1590-1598. *(PELT algorithm)*

2. **Bai, J., & Perron, P. (1998).** "Estimating and testing linear models with multiple structural changes." *Econometrica*, 47-78.

3. **Scott, A. J., & Knott, M. (1974).** "A cluster analysis method for grouping means in the analysis of variance." *Biometrics*, 507-512. *(Binary Segmentation)*

### Domain-Specific Applications
4. **Hamilton, J. D. (2008).** "Oil and the macroeconomy." In *The New Palgrave Dictionary of Economics*.

5. **Kilian, L. (2009).** "Not all oil price shocks are alike: Disentangling demand and supply shocks in the crude oil market." *American Economic Review*, 99(3), 1053-1069.

### Practical Implementation
6. **Killick, R., & Eckley, I. (2014).** "changepoint: An R package for changepoint analysis." *Journal of Statistical Software*, 58(3), 1-19.

7. **Truong, C., Oudre, L., & Vayatis, N. (2020).** "Selective review of offline change point detection methods." *Signal Processing*, 167, 107299.

---

## 5. Preliminary Data Requirements

Before modeling, ensure data includes:
- **Date range**: Minimum 1987-01-01 to present for daily data
- **Missing values**: <2% missingness; no gaps exceeding 5 consecutive trading days
- **Price field**: Daily closing prices in USD per barrel
- **Volume data**: Optional but useful for validating break significance
- **Event annotations**: External CSV with dates and descriptions (see references/geopolitical_events.csv)
