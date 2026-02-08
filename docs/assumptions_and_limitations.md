# Assumptions and Limitations

## Document Purpose
This document outlines the critical assumptions underlying the Brent oil price change point analysis and the inherent limitations that affect interpretation of results. Understanding these constraints is essential for stakeholders to make informed decisions based on the analysis outputs.

---

## Core Assumptions

### 1. Data Quality Assumptions
- **Assumption**: The Brent oil price data represents accurate daily market closing prices without systematic bias
- **Assumption**: Missing data points are randomly distributed and not clustered during crisis periods
- **Assumption**: Historical prices reflect genuine market transactions rather than reporting artifacts
- **Risk**: If data quality is poor, detected change points may reflect measurement errors rather than true structural breaks

### 2. Temporal Independence Assumptions
- **Assumption**: Change point detection algorithms assume observations are conditionally independent given regime
- **Assumption**: Autocorrelation in returns is adequately captured by model specification
- **Risk**: Strong serial correlation can lead to spurious change point detections or missed breaks

### 3. Event Attribution Assumptions
- **Assumption**: Major geopolitical events are primary drivers of structural price breaks
- **Assumption**: Events in the compiled dataset represent exogenous shocks rather than endogenous market developments
- **Risk**: Multiple simultaneous factors (seasonal patterns, inventory cycles) may confound event attribution

### 4. Model Specification Assumptions
- **Assumption**: Price dynamics can be adequately modeled using piecewise constant or piecewise linear segments
- **Assumption**: A single penalty parameter adequately balances detection sensitivity across different time periods
- **Assumption**: Change points occur instantaneously rather than through gradual transitions

---

## Critical Distinction: Correlation vs. Causation

### The Fundamental Challenge
A central limitation of this analysis is that **detecting temporal proximity between events and change points does not prove causation**. This distinction requires careful consideration:

| Correlation Evidence | Causation Requirements |
|---------------------|----------------------|
| Event date aligns with detected change point (±30-90 days) | Demonstrated causal mechanism linking event to price change |
| Statistical significance of temporal clustering | Temporal precedence (event precedes price change) |
| Granger causality test significance | Elimination of alternative explanations |
| Visual pattern matching | Counterfactual analysis (what would have happened without event) |

### Why This Matters for Oil Price Analysis
1. **Confounding Variables**: Oil prices are influenced by dozens of factors simultaneously. A detected change point may coincide with an OPEC decision but actually be driven by:
   - Inventory report surprises
   - USD exchange rate movements
   - Competing energy source price changes
   - Algorithmic trading cascades

2. **Reverse Causality**: Sometimes price movements cause events rather than vice versa. For example, sustained low prices may prompt OPEC to cut production—the causality runs from price to policy, not policy to price.

3. **Selection Bias**: We compile known major events but may miss:
   - Smaller cumulative events that collectively drive change
   - "Black swan" events not in historical records
   - Market regime changes without clear triggering events

4. **Multiple Testing Problem**: When testing 15+ events against detected change points, some apparent alignments will occur by chance alone.

### Best Practices for Interpretation
- **Language**: Use "associated with" or "coincided with" rather than "caused by"
- **Confidence Levels**: Report temporal alignment probabilities, not binary causation claims
- **Mechanism Documentation**: When strong alignment found, research and document the specific transmission mechanism
- **Alternative Hypotheses**: For each significant alignment, explicitly consider 2-3 alternative explanations

---

## Methodological Limitations

### Change Point Detection Limitations
| Limitation | Impact | Mitigation Strategy |
|-----------|--------|-------------------|
| False positive detections during volatility clustering | Misidentification of random noise as structural breaks | Apply post-processing filters requiring minimum regime duration |
| Insufficient power near series endpoints | May miss recent changes or early historical breaks | Use specialized boundary correction methods |
| Multiple change points affect each other's detection | Sequentially detected points may be suboptimal jointly | Use global optimization (PELT) rather than greedy methods |
| Assumes abrupt changes | Gradual regime transitions may be poorly detected | Consider smooth transition autoregressive (STAR) models |

### Statistical Inference Limitations
- Confidence intervals for change point locations are often wide (±months)
- Asymptotic theory may not hold for short series segments
- Bootstrap methods assume stationarity within regimes
- Multiple structural breaks reduce estimation precision

### Data Limitations
- Daily data available only from ~1987 onwards; earlier analysis uses monthly aggregation
- Brent benchmark relevance varies over time (WTI vs Brent spread changes)
- Intraday volatility not captured in daily closing prices
- Geopolitical event dates are approximate (announcement vs implementation vs market reaction)

---

## Scope Limitations

### What This Analysis CANNOT Do
1. **Predict future change points**: Models are descriptive, not predictive
2. **Forecast price levels**: Identifies regime changes but not price direction within regimes
3. **Quantify exact price impacts**: Effect sizes confounded by multiple factors
4. **Capture all structural breaks**: Subtle changes below detection sensitivity threshold will be missed
5. **Establish policy counterfactuals**: Cannot definitively say "what would have happened if OPEC had not acted"

### Appropriate vs. Inappropriate Uses

| Appropriate Use | Inappropriate Use |
|-----------------|-----------------|
| Identifying periods requiring further investigation | Making definitive causal claims without additional evidence |
| Generating hypotheses about event impacts | Using detected points for automated trading without validation |
| Documenting historical regime changes | Extrapolating patterns to future regimes |
| Flagging dates for event study analysis | Blaming specific actors for price movements |
| Risk management stress testing | Legal or regulatory action justification |

---

## Recommendations for Stakeholders

### Risk Managers
- Use change points as indicators for regime-switching model recalibration
- Do not base position sizing solely on detected break dates
- Incorporate 30-90 day uncertainty windows around reported dates

### Policy Analysts
- Treat event-alignment findings as starting points for deeper investigation
- Consider non-oil-specific macro factors in parallel analysis
- Acknowledge uncertainty when briefing decision-makers

### Researchers
- Plan follow-up event study methodology for high-priority alignments
- Document alternative explanations in publications
- Provide sensitivity analysis around key assumptions

---

## Revision History
- v1.0: Initial assumptions and limitations documentation
- Next review: Upon completion of preliminary analysis results
