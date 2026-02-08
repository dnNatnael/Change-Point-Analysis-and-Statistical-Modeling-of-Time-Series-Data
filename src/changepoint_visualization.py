"""
Change Point Visualization Module
===================================
Specialized visualization functions for Bayesian change point analysis results.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import arviz as az
from typing import List, Dict, Tuple, Optional
from datetime import datetime

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10


def plot_changepoint_posterior(model, 
                               bins: int = 50,
                               figsize: Tuple[int, int] = (14, 6)) -> plt.Figure:
    """
    Plot the posterior distribution of the change point (tau).
    
    Parameters
    ----------
    model : BayesianChangePointModel
        Fitted Bayesian change point model
    bins : int
        Number of bins for histogram
    figsize : Tuple[int, int]
        Figure size
    
    Returns
    -------
    plt.Figure
        Matplotlib figure
    """
    tau_posterior = model.get_change_point_posterior()
    tau_idx, tau_date = model.get_change_point_estimate(method='mode')
    
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Histogram of tau (as indices)
    tau_indices = model.trace.posterior['tau'].values.flatten()
    axes[0].hist(tau_indices, bins=bins, alpha=0.7, color='steelblue', edgecolor='black')
    axes[0].axvline(tau_idx, color='red', linestyle='--', linewidth=2, 
                    label=f'Mode: {tau_date.strftime("%Y-%m-%d")}')
    axes[0].set_xlabel('Time Index')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Posterior Distribution of Change Point (τ)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Histogram of tau (as dates) - showing top dates
    date_counts = tau_posterior.value_counts().sort_values(ascending=False).head(20)
    axes[1].barh(range(len(date_counts)), date_counts.values, color='steelblue', alpha=0.7)
    axes[1].set_yticks(range(len(date_counts)))
    axes[1].set_yticklabels([d.strftime('%Y-%m-%d') for d in date_counts.index], fontsize=8)
    axes[1].set_xlabel('Frequency')
    axes[1].set_title('Top 20 Most Probable Change Point Dates')
    axes[1].grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    
    return fig


def plot_parameter_posteriors(model, 
                              figsize: Tuple[int, int] = (14, 8)) -> plt.Figure:
    """
    Plot posterior distributions for before/after parameters.
    
    Parameters
    ----------
    model : BayesianChangePointModel
        Fitted Bayesian change point model
    figsize : Tuple[int, int]
        Figure size
    
    Returns
    -------
    plt.Figure
        Matplotlib figure
    """
    posteriors = model.get_parameter_posteriors()
    impact = model.compute_impact()
    
    # Determine which parameters to plot
    param_pairs = []
    if 'mu_before' in posteriors and 'mu_after' in posteriors:
        param_pairs.append(('mu_before', 'mu_after', 'Mean'))
    if 'sigma_before' in posteriors and 'sigma_after' in posteriors:
        param_pairs.append(('sigma_before', 'sigma_after', 'Std Dev'))
    
    n_params = len(param_pairs)
    if n_params == 0:
        raise ValueError("No before/after parameters found in model")
    
    fig, axes = plt.subplots(n_params, 2, figsize=figsize)
    if n_params == 1:
        axes = axes.reshape(1, -1)
    
    for i, (param_before, param_after, label) in enumerate(param_pairs):
        # Posterior distributions
        ax1 = axes[i, 0]
        ax1.hist(posteriors[param_before], bins=50, alpha=0.6, 
                label=f'Before', color='blue', density=True)
        ax1.hist(posteriors[param_after], bins=50, alpha=0.6, 
                label=f'After', color='red', density=True)
        ax1.axvline(posteriors[param_before].mean(), color='blue', 
                   linestyle='--', linewidth=2)
        ax1.axvline(posteriors[param_after].mean(), color='red', 
                   linestyle='--', linewidth=2)
        ax1.set_xlabel(f'{label} Value')
        ax1.set_ylabel('Density')
        ax1.set_title(f'Posterior Distribution: {label}')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Difference distribution
        ax2 = axes[i, 1]
        diff = posteriors[param_after] - posteriors[param_before]
        ax2.hist(diff, bins=50, alpha=0.7, color='green', edgecolor='black', density=True)
        ax2.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
        ax2.axvline(diff.mean(), color='red', linestyle='--', linewidth=2, 
                   label=f'Mean: {diff.mean():.4f}')
        
        # Add credible interval
        ci_lower, ci_upper = np.percentile(diff, [2.5, 97.5])
        ax2.axvspan(ci_lower, ci_upper, alpha=0.2, color='green', 
                   label=f'95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]')
        
        ax2.set_xlabel(f'{label} Change (After - Before)')
        ax2.set_ylabel('Density')
        ax2.set_title(f'Posterior Distribution: {label} Change')
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    return fig


def plot_data_with_changepoint(data: pd.Series,
                               model,
                               events: Optional[pd.DataFrame] = None,
                               figsize: Tuple[int, int] = (16, 8)) -> plt.Figure:
    """
    Plot time series data with detected change point and regime means.
    
    Parameters
    ----------
    data : pd.Series
        Original time series data
    model : BayesianChangePointModel
        Fitted Bayesian change point model
    events : pd.DataFrame, optional
        Geopolitical events to overlay
    figsize : Tuple[int, int]
        Figure size
    
    Returns
    -------
    plt.Figure
        Matplotlib figure
    """
    tau_idx, tau_date = model.get_change_point_estimate(method='mode')
    impact = model.compute_impact()
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot data
    ax.plot(data.index, data.values, color='gray', alpha=0.5, linewidth=1, label='Data')
    
    # Plot regime means
    mu_before = impact.get('mu_before', 0)
    mu_after = impact.get('mu_after', 0)
    
    before_dates = data.index[data.index < tau_date]
    after_dates = data.index[data.index >= tau_date]
    
    if len(before_dates) > 0:
        ax.hlines(mu_before, before_dates[0], tau_date, 
                 colors='blue', linewidth=3, label=f'Before Mean: {mu_before:.4f}')
    if len(after_dates) > 0:
        ax.hlines(mu_after, tau_date, after_dates[-1], 
                 colors='red', linewidth=3, label=f'After Mean: {mu_after:.4f}')
    
    # Mark change point
    ax.axvline(tau_date, color='green', linestyle='--', linewidth=2, 
              label=f'Change Point: {tau_date.strftime("%Y-%m-%d")}')
    
    # Add shaded regions for regimes
    if len(before_dates) > 0:
        ax.axvspan(before_dates[0], tau_date, alpha=0.1, color='blue')
    if len(after_dates) > 0:
        ax.axvspan(tau_date, after_dates[-1], alpha=0.1, color='red')
    
    # Overlay events if provided
    if events is not None:
        for idx, event in events.iterrows():
            if data.index.min() <= idx <= data.index.max():
                ax.axvline(idx, color='orange', alpha=0.3, linestyle=':', linewidth=1)
                # Add event label (rotated)
                y_pos = ax.get_ylim()[1] * 0.95
                ax.text(idx, y_pos, event.get('Event', ''), 
                       rotation=90, verticalalignment='top', 
                       fontsize=7, alpha=0.7)
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    ax.set_title(f'Time Series with Detected Change Point\n'
                f'Mean Change: {impact.get("mu_change", 0):.4f} '
                f'({impact.get("mu_pct_change", 0):.2f}%)')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    return fig


def plot_convergence_diagnostics(model, 
                                 figsize: Tuple[int, int] = (16, 10)) -> plt.Figure:
    """
    Plot comprehensive convergence diagnostics.
    
    Parameters
    ----------
    model : BayesianChangePointModel
        Fitted Bayesian change point model
    figsize : Tuple[int, int]
        Figure size
    
    Returns
    -------
    plt.Figure
        Matplotlib figure
    """
    if model.trace is None:
        raise ValueError("No trace available. Run sample() first.")
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=figsize)
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # 1. Trace plots
    ax1 = fig.add_subplot(gs[0, :])
    tau_samples = model.trace.posterior['tau'].values
    for chain in range(tau_samples.shape[0]):
        ax1.plot(tau_samples[chain, :], alpha=0.7, label=f'Chain {chain+1}')
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('τ (Change Point Index)')
    ax1.set_title('MCMC Trace Plot for τ')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Autocorrelation plot
    ax2 = fig.add_subplot(gs[1, 0])
    tau_flat = tau_samples.flatten()
    az.plot_autocorr(model.trace, var_names=['tau'], ax=ax2)
    ax2.set_title('Autocorrelation: τ')
    
    # 3. R-hat values
    ax3 = fig.add_subplot(gs[1, 1])
    summary = model.summary
    r_hat_values = summary['r_hat'].dropna()
    ax3.bar(range(len(r_hat_values)), r_hat_values.values, color='steelblue', alpha=0.7)
    ax3.axhline(1.0, color='green', linestyle='--', linewidth=2, label='Target')
    ax3.axhline(1.01, color='orange', linestyle='--', linewidth=1, label='Threshold')
    ax3.set_xticks(range(len(r_hat_values)))
    ax3.set_xticklabels(r_hat_values.index, rotation=45, ha='right', fontsize=8)
    ax3.set_ylabel('R-hat')
    ax3.set_title('Gelman-Rubin Convergence Diagnostic (R-hat)')
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. Effective Sample Size
    ax4 = fig.add_subplot(gs[2, 0])
    ess_bulk = summary['ess_bulk'].dropna()
    ax4.bar(range(len(ess_bulk)), ess_bulk.values, color='green', alpha=0.7)
    ax4.axhline(400, color='red', linestyle='--', linewidth=1, label='Min Threshold')
    ax4.set_xticks(range(len(ess_bulk)))
    ax4.set_xticklabels(ess_bulk.index, rotation=45, ha='right', fontsize=8)
    ax4.set_ylabel('ESS Bulk')
    ax4.set_title('Effective Sample Size (Bulk)')
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    
    # 5. Energy plot
    ax5 = fig.add_subplot(gs[2, 1])
    az.plot_energy(model.trace, ax=ax5)
    ax5.set_title('Energy Plot')
    
    plt.tight_layout()
    
    return fig


def plot_multiple_changepoints(data: pd.Series,
                               models: List,
                               events: Optional[pd.DataFrame] = None,
                               figsize: Tuple[int, int] = (16, 10)) -> plt.Figure:
    """
    Plot time series with multiple detected change points.
    
    Parameters
    ----------
    data : pd.Series
        Original time series data
    models : List[BayesianChangePointModel]
        List of fitted models
    events : pd.DataFrame, optional
        Geopolitical events to overlay
    figsize : Tuple[int, int]
        Figure size
    
    Returns
    -------
    plt.Figure
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot data
    ax.plot(data.index, data.values, color='gray', alpha=0.5, 
           linewidth=1, label='Data', zorder=1)
    
    # Collect all change points
    change_points = []
    for i, model in enumerate(models):
        tau_idx, tau_date = model.get_change_point_estimate(method='mode')
        change_points.append((tau_date, i+1))
        
        # Mark change point
        ax.axvline(tau_date, color=f'C{i}', linestyle='--', linewidth=2, 
                  label=f'CP {i+1}: {tau_date.strftime("%Y-%m-%d")}', zorder=3)
    
    # Sort change points
    change_points.sort(key=lambda x: x[0])
    
    # Add regime labels
    for i in range(len(change_points) + 1):
        if i == 0:
            start = data.index[0]
            end = change_points[0][0] if change_points else data.index[-1]
        elif i == len(change_points):
            start = change_points[-1][0]
            end = data.index[-1]
        else:
            start = change_points[i-1][0]
            end = change_points[i][0]
        
        # Shade regime
        ax.axvspan(start, end, alpha=0.1, color=f'C{i}', zorder=0)
        
        # Add regime label
        mid_point = start + (end - start) / 2
        y_pos = ax.get_ylim()[1] * 0.95
        ax.text(mid_point, y_pos, f'Regime {i+1}', 
               horizontalalignment='center', fontsize=10, 
               fontweight='bold', bbox=dict(boxstyle='round', 
               facecolor=f'C{i}', alpha=0.3))
    
    # Overlay events if provided
    if events is not None:
        for idx, event in events.iterrows():
            if data.index.min() <= idx <= data.index.max():
                ax.axvline(idx, color='orange', alpha=0.2, 
                          linestyle=':', linewidth=1, zorder=2)
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Value')
    ax.set_title(f'Time Series with {len(models)} Detected Change Points')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    return fig


def create_impact_summary_table(models: List,
                                events: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Create a summary table of change point impacts.
    
    Parameters
    ----------
    models : List[BayesianChangePointModel]
        List of fitted models
    events : pd.DataFrame, optional
        Geopolitical events for matching
    
    Returns
    -------
    pd.DataFrame
        Summary table with change points and impacts
    """
    summary_data = []
    
    for i, model in enumerate(models):
        tau_idx, tau_date = model.get_change_point_estimate(method='mode')
        impact = model.compute_impact()
        
        row = {
            'Change Point': i + 1,
            'Date': tau_date.strftime('%Y-%m-%d'),
            'Mean Before': impact.get('mu_before', np.nan),
            'Mean After': impact.get('mu_after', np.nan),
            'Mean Change': impact.get('mu_change', np.nan),
            'Mean % Change': impact.get('mu_pct_change', np.nan),
            'Cohen\'s d': impact.get('cohens_d', np.nan)
        }
        
        # Add variance info if available
        if 'sigma_before' in impact:
            row['Std Before'] = impact['sigma_before']
            row['Std After'] = impact['sigma_after']
            row['Std Change'] = impact['sigma_change']
        
        # Match with nearest event
        if events is not None:
            time_diffs = abs((events.index - tau_date).total_seconds())
            nearest_idx = time_diffs.argmin()
            nearest_event = events.iloc[nearest_idx]
            days_diff = time_diffs.iloc[nearest_idx] / (24 * 3600)
            
            if days_diff <= 30:  # Within 30 days
                row['Nearest Event'] = nearest_event.get('Event', 'Unknown')
                row['Event Date'] = events.index[nearest_idx].strftime('%Y-%m-%d')
                row['Days from Event'] = int(days_diff)
        
        summary_data.append(row)
    
    return pd.DataFrame(summary_data)


def plot_impact_comparison(models: List,
                          figsize: Tuple[int, int] = (14, 6)) -> plt.Figure:
    """
    Compare impacts across multiple change points.
    
    Parameters
    ----------
    models : List[BayesianChangePointModel]
        List of fitted models
    figsize : Tuple[int, int]
        Figure size
    
    Returns
    -------
    plt.Figure
        Matplotlib figure
    """
    impacts = [model.compute_impact() for model in models]
    
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Mean changes
    ax1 = axes[0]
    cp_labels = [f'CP {i+1}' for i in range(len(models))]
    mean_changes = [imp.get('mu_change', 0) for imp in impacts]
    colors = ['green' if x > 0 else 'red' for x in mean_changes]
    
    ax1.barh(cp_labels, mean_changes, color=colors, alpha=0.7)
    ax1.axvline(0, color='black', linestyle='--', linewidth=1)
    ax1.set_xlabel('Mean Change')
    ax1.set_title('Mean Change at Each Change Point')
    ax1.grid(True, alpha=0.3, axis='x')
    
    # Effect sizes (Cohen's d)
    ax2 = axes[1]
    cohens_d = [imp.get('cohens_d', 0) for imp in impacts]
    colors = ['green' if abs(x) > 0.8 else 'orange' if abs(x) > 0.5 else 'gray' 
             for x in cohens_d]
    
    ax2.barh(cp_labels, cohens_d, color=colors, alpha=0.7)
    ax2.axvline(0, color='black', linestyle='--', linewidth=1)
    ax2.axvline(0.5, color='orange', linestyle=':', linewidth=1, alpha=0.5, label='Medium')
    ax2.axvline(0.8, color='green', linestyle=':', linewidth=1, alpha=0.5, label='Large')
    ax2.axvline(-0.5, color='orange', linestyle=':', linewidth=1, alpha=0.5)
    ax2.axvline(-0.8, color='green', linestyle=':', linewidth=1, alpha=0.5)
    ax2.set_xlabel('Effect Size (Cohen\'s d)')
    ax2.set_title('Effect Size at Each Change Point')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    
    return fig


if __name__ == "__main__":
    print("Change Point Visualization Module")
    print("Provides specialized plotting functions for Bayesian change point analysis.")
