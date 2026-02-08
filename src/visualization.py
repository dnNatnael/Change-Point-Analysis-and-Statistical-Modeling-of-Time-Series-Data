"""
Visualization Module
=====================
Creates publication-quality visualizations for time series analysis:
- Price trend plots with moving averages
- Volatility analysis plots
- Stationarity diagnostic plots
- Event overlay plots
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter, YearLocator
from typing import Optional, List, Dict
import logging

logger = logging.getLogger(__name__)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class VisualizationError(Exception):
    """Custom exception for visualization errors."""
    pass


def plot_price_trend(df: pd.DataFrame,
                    price_col: str = 'Price',
                    ma_windows: List[int] = [30, 90, 252],
                    figsize: tuple = (15, 8),
                    title: str = "Brent Oil Price Trend",
                    save_path: Optional[str] = None) -> plt.Figure:
    """
    Plot price trend with moving averages.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with price and date index.
    price_col : str
        Column name for price data.
    ma_windows : List[int]
        Moving average window sizes to plot.
    figsize : tuple
        Figure size (width, height).
    title : str
        Plot title.
    save_path : str, optional
        Path to save figure.
    
    Returns
    -------
    plt.Figure
        Matplotlib figure object.
    """
    try:
        logger.info("Creating price trend plot")
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot price
        ax.plot(df.index, df[price_col], label='Price', linewidth=1.2, alpha=0.9)
        
        # Plot moving averages
        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(ma_windows)))
        for window, color in zip(ma_windows, colors):
            ma_col = f'MA_{window}'
            if ma_col in df.columns:
                ax.plot(df.index, df[ma_col], 
                       label=f'{window}-day MA', 
                       linewidth=1.5, 
                       color=color,
                       linestyle='--')
        
        # Formatting
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price (USD per barrel)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis
        ax.xaxis.set_major_locator(YearLocator(5))
        ax.xaxis.set_major_formatter(DateFormatter('%Y'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved plot to {save_path}")
        
        return fig
    
    except Exception as e:
        raise VisualizationError(f"Error creating price trend plot: {e}")


def plot_returns_distribution(df: pd.DataFrame,
                             return_col: str = 'Log_Returns',
                             figsize: tuple = (15, 10),
                             save_path: Optional[str] = None) -> plt.Figure:
    """
    Plot returns distribution with histogram and Q-Q plot.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with returns column.
    return_col : str
        Column name for returns.
    figsize : tuple
        Figure size.
    save_path : str, optional
        Path to save figure.
    
    Returns
    -------
    plt.Figure
        Matplotlib figure object.
    """
    try:
        logger.info("Creating returns distribution plot")
        
        returns = df[return_col].dropna()
        
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        
        # Time series of returns
        ax1 = axes[0, 0]
        ax1.plot(returns.index, returns, linewidth=0.8, alpha=0.7)
        ax1.axhline(y=0, color='r', linestyle='-', alpha=0.3)
        ax1.set_title('Log Returns Time Series', fontweight='bold')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Log Return')
        ax1.grid(True, alpha=0.3)
        
        # Histogram with normal overlay
        ax2 = axes[0, 1]
        ax2.hist(returns, bins=100, density=True, alpha=0.7, color='steelblue', edgecolor='black')
        
        # Overlay normal distribution
        mu, sigma = returns.mean(), returns.std()
        x = np.linspace(returns.min(), returns.max(), 100)
        normal_curve = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
        ax2.plot(x, normal_curve, 'r-', linewidth=2, label='Normal Distribution')
        ax2.set_title('Returns Distribution', fontweight='bold')
        ax2.set_xlabel('Log Return')
        ax2.set_ylabel('Density')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Box plot
        ax3 = axes[1, 0]
        ax3.boxplot(returns, vert=True)
        ax3.set_title('Returns Box Plot', fontweight='bold')
        ax3.set_ylabel('Log Return')
        ax3.grid(True, alpha=0.3)
        
        # Q-Q plot
        ax4 = axes[1, 1]
        from scipy import stats
        stats.probplot(returns, dist="norm", plot=ax4)
        ax4.set_title('Q-Q Plot (vs Normal)', fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        plt.suptitle(f'{return_col} Analysis', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved plot to {save_path}")
        
        return fig
    
    except Exception as e:
        raise VisualizationError(f"Error creating returns distribution plot: {e}")


def plot_volatility_analysis(df: pd.DataFrame,
                            vol_cols: Optional[List[str]] = None,
                            price_col: str = 'Price',
                            figsize: tuple = (15, 10),
                            save_path: Optional[str] = None) -> plt.Figure:
    """
    Plot volatility analysis with regime classification.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with price and volatility columns.
    vol_cols : List[str], optional
        Volatility column names. If None, uses all Volatility_* columns.
    price_col : str
        Price column name.
    figsize : tuple
        Figure size.
    save_path : str, optional
        Path to save figure.
    
    Returns
    -------
    plt.Figure
        Matplotlib figure object.
    """
    try:
        logger.info("Creating volatility analysis plot")
        
        # Auto-detect volatility columns if not specified
        if vol_cols is None:
            vol_cols = [col for col in df.columns if col.startswith('Volatility_')]
        
        fig, axes = plt.subplots(3, 1, figsize=figsize, sharex=True)
        
        # Price with volatility bands
        ax1 = axes[0]
        ax1.plot(df.index, df[price_col], label='Price', color='black', linewidth=1)
        
        if 'BB_Upper' in df.columns:
            ax1.fill_between(df.index, df['BB_Lower'], df['BB_Upper'], 
                           alpha=0.2, color='blue', label='Bollinger Bands')
        
        ax1.set_ylabel('Price (USD)', fontsize=11)
        ax1.set_title('Price with Volatility Bands', fontweight='bold', fontsize=12)
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # Volatility time series
        ax2 = axes[1]
        colors = plt.cm.plasma(np.linspace(0.2, 0.8, len(vol_cols)))
        
        for vol_col, color in zip(vol_cols, colors):
            ax2.plot(df.index, df[vol_col], label=vol_col.replace('Volatility_', ''), 
                    linewidth=1.2, color=color, alpha=0.8)
        
        ax2.set_ylabel('Annualized Volatility', fontsize=11)
        ax2.set_title('Rolling Volatility (Different Windows)', fontweight='bold', fontsize=12)
        ax2.legend(loc='upper right', title='Window (days)')
        ax2.grid(True, alpha=0.3)
        
        # Volatility regime
        if 'Volatility_Regime' in df.columns:
            ax3 = axes[2]
            
            # Create color mapping for regimes
            regime_colors = {'Low': 'green', 'Medium': 'orange', 'High': 'red', 'Unknown': 'gray'}
            
            for regime in df['Volatility_Regime'].unique():
                if pd.notna(regime):
                    mask = df['Volatility_Regime'] == regime
                    color = regime_colors.get(regime, 'blue')
                    ax3.fill_between(df.index, 0, 1, where=mask, 
                                   alpha=0.5, color=color, label=f'{regime} Volatility')
            
            ax3.set_ylabel('Regime', fontsize=11)
            ax3.set_title('Volatility Regimes', fontweight='bold', fontsize=12)
            ax3.set_ylim(0, 1)
            ax3.set_yticks([])
            ax3.legend(loc='upper right', title='Regime')
            ax3.grid(True, alpha=0.3)
        else:
            ax3 = axes[2]
            ax3.text(0.5, 0.5, 'Volatility regimes not computed', 
                    ha='center', va='center', transform=ax3.transAxes)
            ax3.set_ylabel('Regime', fontsize=11)
        
        ax3.set_xlabel('Date', fontsize=11)
        
        # Format x-axis
        ax3.xaxis.set_major_locator(YearLocator(5))
        ax3.xaxis.set_major_formatter(DateFormatter('%Y'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved plot to {save_path}")
        
        return fig
    
    except Exception as e:
        raise VisualizationError(f"Error creating volatility plot: {e}")


def plot_stationarity_diagnostics(df: pd.DataFrame,
                                 series_col: str = 'Price',
                                 return_col: str = 'Log_Returns',
                                 figsize: tuple = (15, 12),
                                 save_path: Optional[str] = None) -> plt.Figure:
    """
    Create comprehensive stationarity diagnostic plots.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with price and returns.
    series_col : str
        Original series column.
    return_col : str
        Returns column.
    figsize : tuple
        Figure size.
    save_path : str, optional
        Path to save figure.
    
    Returns
    -------
    plt.Figure
        Matplotlib figure object.
    """
    try:
        logger.info("Creating stationarity diagnostics plot")
        
        fig, axes = plt.subplots(4, 2, figsize=figsize)
        
        # Original series
        ax = axes[0, 0]
        ax.plot(df.index, df[series_col], color='steelblue', linewidth=1)
        ax.set_title(f'{series_col} - Original Series', fontweight='bold', fontsize=11)
        ax.set_ylabel('Price')
        ax.grid(True, alpha=0.3)
        
        # ACF of original series
        ax = axes[0, 1]
        from statsmodels.graphics.tsaplots import plot_acf
        plot_acf(df[series_col].dropna(), ax=ax, lags=40, title=f'ACF - {series_col}')
        ax.grid(True, alpha=0.3)
        
        # First difference
        ax = axes[1, 0]
        diff_series = df[series_col].diff().dropna()
        ax.plot(diff_series.index, diff_series, color='darkgreen', linewidth=0.8, alpha=0.7)
        ax.axhline(y=0, color='r', linestyle='-', alpha=0.3)
        ax.set_title(f'{series_col} - First Difference', fontweight='bold', fontsize=11)
        ax.set_ylabel('Difference')
        ax.grid(True, alpha=0.3)
        
        # ACF of differenced series
        ax = axes[1, 1]
        plot_acf(diff_series, ax=ax, lags=40, title='ACF - First Difference')
        ax.grid(True, alpha=0.3)
        
        # Log returns
        if return_col in df.columns:
            returns = df[return_col].dropna()
            
            ax = axes[2, 0]
            ax.plot(returns.index, returns, color='purple', linewidth=0.8, alpha=0.7)
            ax.axhline(y=0, color='r', linestyle='-', alpha=0.3)
            ax.set_title(f'{return_col}', fontweight='bold', fontsize=11)
            ax.set_ylabel('Return')
            ax.grid(True, alpha=0.3)
            
            # ACF of returns
            ax = axes[2, 1]
            plot_acf(returns, ax=ax, lags=40, title=f'ACF - {return_col}')
            ax.grid(True, alpha=0.3)
            
            # Squared returns (volatility proxy)
            ax = axes[3, 0]
            ax.plot(returns.index, returns**2, color='darkred', linewidth=0.8, alpha=0.7)
            ax.set_title(f'{return_col}² (Volatility Proxy)', fontweight='bold', fontsize=11)
            ax.set_ylabel('Squared Return')
            ax.set_xlabel('Date')
            ax.grid(True, alpha=0.3)
            
            # ACF of squared returns
            ax = axes[3, 1]
            plot_acf(returns**2, ax=ax, lags=40, title=f'ACF - {return_col}²')
            ax.set_xlabel('Lag')
            ax.grid(True, alpha=0.3)
        
        plt.suptitle('Stationarity Diagnostics', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved plot to {save_path}")
        
        return fig
    
    except Exception as e:
        raise VisualizationError(f"Error creating stationarity diagnostics: {e}")


def plot_events_overlay(df: pd.DataFrame,
                       events_df: pd.DataFrame,
                       price_col: str = 'Price',
                       figsize: tuple = (18, 10),
                       window_days: int = 90,
                       save_path: Optional[str] = None) -> plt.Figure:
    """
    Plot price series with event markers overlaid.
    
    Parameters
    ----------
    df : pd.DataFrame
        Price DataFrame.
    events_df : pd.DataFrame
        Events DataFrame with Event_Date index.
    price_col : str
        Price column name.
    figsize : tuple
        Figure size.
    window_days : int
        Days to show around each event (for zoomed views).
    save_path : str, optional
        Path to save figure.
    
    Returns
    -------
    plt.Figure
        Matplotlib figure object.
    """
    try:
        logger.info(f"Creating events overlay plot with {len(events_df)} events")
        
        # Create main overview plot
        fig, axes = plt.subplots(2, 1, figsize=figsize, gridspec_kw={'height_ratios': [3, 1]})
        
        # Main price plot
        ax1 = axes[0]
        ax1.plot(df.index, df[price_col], color='black', linewidth=1, alpha=0.8)
        
        # Color map for event types
        event_colors = {
            'OPEC Policy': 'red',
            'Geopolitical': 'orange',
            'Financial': 'blue',
            'Natural Disaster': 'green',
            'Policy': 'purple'
        }
        
        # Add event markers
        for idx, event in events_df.iterrows():
            event_date = idx
            event_name = event.get('Event_Name', 'Unknown')
            event_type = event.get('Event_Type', 'Unknown')
            color = event_colors.get(event_type, 'gray')
            
            # Find closest date in price data
            if event_date in df.index:
                price_at_event = df.loc[event_date, price_col]
            else:
                # Find nearest date
                nearest_idx = df.index.get_indexer([event_date], method='nearest')[0]
                if nearest_idx >= 0:
                    nearest_date = df.index[nearest_idx]
                    price_at_event = df.loc[nearest_date, price_col]
                else:
                    continue
            
            ax1.axvline(x=event_date, color=color, linestyle='--', alpha=0.6, linewidth=1)
            ax1.scatter([event_date], [price_at_event], color=color, s=50, zorder=5)
        
        ax1.set_ylabel('Price (USD)', fontsize=11)
        ax1.set_title('Brent Oil Price with Major Events', fontweight='bold', fontsize=13)
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='upper left')
        
        # Event timeline
        ax2 = axes[1]
        y_pos = 0
        for idx, event in events_df.iterrows():
            event_date = idx
            event_name = event.get('Event_Name', 'Unknown')
            event_type = event.get('Event_Type', 'Unknown')
            color = event_colors.get(event_type, 'gray')
            
            ax2.barh(y_pos, 1, left=event_date, color=color, alpha=0.7, height=0.5)
            ax2.text(event_date, y_pos, event_name, fontsize=7, va='center', ha='left', rotation=45)
            y_pos += 1
        
        ax2.set_xlabel('Date', fontsize=11)
        ax2.set_title('Event Timeline', fontweight='bold', fontsize=11)
        ax2.set_yticks([])
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Add legend for event types
        legend_elements = [plt.Line2D([0], [0], color=color, lw=2, label=event_type)
                          for event_type, color in event_colors.items()]
        ax1.legend(handles=legend_elements, loc='upper left', title='Event Types')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved plot to {save_path}")
        
        return fig
    
    except Exception as e:
        raise VisualizationError(f"Error creating events overlay plot: {e}")


if __name__ == "__main__":
    # Example usage
    from data_loader import load_brent_data, compute_log_returns, clean_data, load_events_data
    from time_series_analysis import compute_volatility, detect_volatility_regimes, compute_rolling_statistics
    
    try:
        # Load data
        df = load_brent_data("../data/raw/BrentOilPrices.csv")
        df_clean = clean_data(df, fill_method='linear')
        df_returns = compute_log_returns(df_clean)
        df_vol = compute_volatility(df_returns)
        df_regimes = detect_volatility_regimes(df_vol)
        df_rolling = compute_rolling_statistics(df_regimes)
        
        # Create plots
        plot_price_trend(df_rolling, save_path="../outputs/price_trend.png")
        plot_returns_distribution(df_returns, save_path="../outputs/returns_distribution.png")
        plot_volatility_analysis(df_regimes, save_path="../outputs/volatility_analysis.png")
        plot_stationarity_diagnostics(df_returns, save_path="../outputs/stationarity_diagnostics.png")
        
        # Load events and overlay
        events_df = load_events_data("../references/geopolitical_events.csv")
        plot_events_overlay(df_clean, events_df, save_path="../outputs/events_overlay.png")
        
        plt.show()
        
    except Exception as e:
        logger.error(f"Error in visualization: {e}")
