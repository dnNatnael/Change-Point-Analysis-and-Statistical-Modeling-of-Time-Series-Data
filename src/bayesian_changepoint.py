"""
Bayesian Change Point Detection Module
========================================
Implements Bayesian change point detection using PyMC for identifying
structural breaks in Brent oil price time series data.
"""

import numpy as np
import pandas as pd
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Tuple, Optional, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class BayesianChangePointModel:
    """
    Bayesian Change Point Detection Model using PyMC.
    
    This model identifies structural breaks in time series data by:
    1. Defining a discrete uniform prior over possible change points
    2. Modeling different parameters before and after the change point
    3. Using MCMC sampling to estimate posterior distributions
    """
    
    def __init__(self, data: pd.Series, name: str = "ChangePoint"):
        """
        Initialize the Bayesian change point model.
        
        Parameters
        ----------
        data : pd.Series
            Time series data (should be stationary or log returns)
        name : str
            Name for the model
        """
        self.data = data.dropna().values
        self.dates = data.dropna().index
        self.n = len(self.data)
        self.name = name
        self.model = None
        self.trace = None
        self.summary = None
        
        logger.info(f"Initialized {name} model with {self.n} observations")
    
    def build_model(self, 
                    model_type: str = "mean_shift",
                    prior_tau_alpha: float = 1.0,
                    prior_tau_beta: float = 1.0) -> pm.Model:
        """
        Build the Bayesian change point model.
        
        Parameters
        ----------
        model_type : str
            Type of model: 'mean_shift' (change in mean) or 
            'mean_variance_shift' (change in both mean and variance)
        prior_tau_alpha : float
            Alpha parameter for tau prior (uniform by default)
        prior_tau_beta : float
            Beta parameter for tau prior (uniform by default)
        
        Returns
        -------
        pm.Model
            PyMC model object
        """
        logger.info(f"Building {model_type} model...")
        
        with pm.Model() as model:
            # Define the change point (tau) as discrete uniform
            # tau can be any day from 0 to n-1
            tau = pm.DiscreteUniform('tau', lower=0, upper=self.n - 1)
            
            if model_type == "mean_shift":
                # Model with change in mean only
                
                # Priors for means before and after change point
                mu_1 = pm.Normal('mu_before', mu=0, sigma=10)
                mu_2 = pm.Normal('mu_after', mu=0, sigma=10)
                
                # Prior for standard deviation (assumed constant)
                sigma = pm.HalfNormal('sigma', sigma=10)
                
                # Switch function: select mu_1 if t < tau, else mu_2
                idx = np.arange(self.n)
                mu = pm.math.switch(tau >= idx, mu_1, mu_2)
                
                # Likelihood
                obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=self.data)
                
            elif model_type == "mean_variance_shift":
                # Model with change in both mean and variance
                
                # Priors for means
                mu_1 = pm.Normal('mu_before', mu=0, sigma=10)
                mu_2 = pm.Normal('mu_after', mu=0, sigma=10)
                
                # Priors for standard deviations
                sigma_1 = pm.HalfNormal('sigma_before', sigma=10)
                sigma_2 = pm.HalfNormal('sigma_after', sigma=10)
                
                # Switch functions
                idx = np.arange(self.n)
                mu = pm.math.switch(tau >= idx, mu_1, mu_2)
                sigma = pm.math.switch(tau >= idx, sigma_1, sigma_2)
                
                # Likelihood
                obs = pm.Normal('obs', mu=mu, sigma=sigma, observed=self.data)
            
            else:
                raise ValueError(f"Unknown model_type: {model_type}")
            
            self.model = model
            logger.info("Model built successfully")
            
        return model
    
    def sample(self, 
               draws: int = 2000,
               tune: int = 1000,
               chains: int = 4,
               target_accept: float = 0.95,
               random_seed: int = 42) -> az.InferenceData:
        """
        Run MCMC sampling to estimate posterior distributions.
        
        Parameters
        ----------
        draws : int
            Number of samples to draw per chain
        tune : int
            Number of tuning/burn-in samples
        chains : int
            Number of MCMC chains
        target_accept : float
            Target acceptance rate for NUTS sampler
        random_seed : int
            Random seed for reproducibility
        
        Returns
        -------
        az.InferenceData
            ArviZ InferenceData object containing samples
        """
        if self.model is None:
            raise ValueError("Model not built. Call build_model() first.")
        
        logger.info(f"Starting MCMC sampling: {draws} draws, {tune} tune, {chains} chains")
        
        with self.model:
            self.trace = pm.sample(
                draws=draws,
                tune=tune,
                chains=chains,
                target_accept=target_accept,
                random_state=random_seed,
                return_inferencedata=True
            )
        
        logger.info("Sampling completed")
        
        # Generate summary statistics
        self.summary = az.summary(self.trace)
        logger.info("\nModel Summary:")
        logger.info(f"\n{self.summary}")
        
        return self.trace
    
    def check_convergence(self) -> Dict[str, any]:
        """
        Check MCMC convergence diagnostics.
        
        Returns
        -------
        Dict
            Convergence diagnostics including r_hat, ESS, and warnings
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        logger.info("Checking convergence diagnostics...")
        
        diagnostics = {
            'summary': self.summary,
            'r_hat_ok': True,
            'ess_ok': True,
            'warnings': []
        }
        
        # Check R-hat (should be close to 1.0, ideally < 1.01)
        r_hat_values = self.summary['r_hat'].dropna()
        max_r_hat = r_hat_values.max()
        
        if max_r_hat > 1.01:
            diagnostics['r_hat_ok'] = False
            diagnostics['warnings'].append(
                f"R-hat values exceed 1.01 (max: {max_r_hat:.4f}). "
                "Consider running more samples or increasing tune."
            )
        
        # Check Effective Sample Size (ESS)
        ess_bulk = self.summary['ess_bulk'].min()
        ess_tail = self.summary['ess_tail'].min()
        
        if ess_bulk < 400 or ess_tail < 400:
            diagnostics['ess_ok'] = False
            diagnostics['warnings'].append(
                f"Low ESS detected (bulk: {ess_bulk:.0f}, tail: {ess_tail:.0f}). "
                "Consider running more samples."
            )
        
        if diagnostics['r_hat_ok'] and diagnostics['ess_ok']:
            logger.info("✓ Convergence diagnostics look good!")
        else:
            logger.warning("⚠ Convergence issues detected:")
            for warning in diagnostics['warnings']:
                logger.warning(f"  - {warning}")
        
        return diagnostics
    
    def get_change_point_posterior(self) -> pd.Series:
        """
        Extract posterior distribution of the change point (tau).
        
        Returns
        -------
        pd.Series
            Posterior samples of tau with corresponding dates
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        # Extract tau samples from all chains
        tau_samples = self.trace.posterior['tau'].values.flatten()
        
        # Convert to dates
        tau_dates = [self.dates[int(t)] for t in tau_samples]
        
        return pd.Series(tau_dates, name='tau_posterior')
    
    def get_parameter_posteriors(self) -> Dict[str, np.ndarray]:
        """
        Extract posterior distributions for all model parameters.
        
        Returns
        -------
        Dict
            Dictionary of parameter names and their posterior samples
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        posteriors = {}
        
        for var_name in self.trace.posterior.data_vars:
            posteriors[var_name] = self.trace.posterior[var_name].values.flatten()
        
        return posteriors
    
    def get_change_point_estimate(self, method: str = 'mode') -> Tuple[int, pd.Timestamp]:
        """
        Get point estimate of the change point.
        
        Parameters
        ----------
        method : str
            Estimation method: 'mode' (most frequent), 'mean', or 'median'
        
        Returns
        -------
        Tuple[int, pd.Timestamp]
            Index and date of the estimated change point
        """
        tau_samples = self.trace.posterior['tau'].values.flatten()
        
        if method == 'mode':
            # Most frequent value
            tau_est = int(np.bincount(tau_samples.astype(int)).argmax())
        elif method == 'mean':
            tau_est = int(np.round(tau_samples.mean()))
        elif method == 'median':
            tau_est = int(np.median(tau_samples))
        else:
            raise ValueError(f"Unknown method: {method}")
        
        tau_date = self.dates[tau_est]
        
        logger.info(f"Change point estimate ({method}): {tau_date} (index {tau_est})")
        
        return tau_est, tau_date
    
    def compute_impact(self) -> Dict[str, float]:
        """
        Compute the quantitative impact of the change point.
        
        Returns
        -------
        Dict
            Impact metrics including mean/variance changes and effect sizes
        """
        posteriors = self.get_parameter_posteriors()
        
        impact = {}
        
        # Mean change
        if 'mu_before' in posteriors and 'mu_after' in posteriors:
            mu_before = posteriors['mu_before'].mean()
            mu_after = posteriors['mu_after'].mean()
            mu_change = mu_after - mu_before
            mu_pct_change = (mu_change / abs(mu_before)) * 100 if mu_before != 0 else np.inf
            
            impact['mu_before'] = mu_before
            impact['mu_after'] = mu_after
            impact['mu_change'] = mu_change
            impact['mu_pct_change'] = mu_pct_change
        
        # Variance change (if applicable)
        if 'sigma_before' in posteriors and 'sigma_after' in posteriors:
            sigma_before = posteriors['sigma_before'].mean()
            sigma_after = posteriors['sigma_after'].mean()
            sigma_change = sigma_after - sigma_before
            sigma_pct_change = (sigma_change / sigma_before) * 100
            
            impact['sigma_before'] = sigma_before
            impact['sigma_after'] = sigma_after
            impact['sigma_change'] = sigma_change
            impact['sigma_pct_change'] = sigma_pct_change
        elif 'sigma' in posteriors:
            impact['sigma'] = posteriors['sigma'].mean()
        
        # Effect size (Cohen's d)
        if 'mu_before' in impact and 'mu_after' in impact:
            pooled_std = impact.get('sigma', 
                                   np.sqrt((impact.get('sigma_before', 1)**2 + 
                                           impact.get('sigma_after', 1)**2) / 2))
            cohens_d = impact['mu_change'] / pooled_std
            impact['cohens_d'] = cohens_d
        
        return impact
    
    def plot_trace(self, figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
        """
        Plot trace plots for convergence diagnostics.
        
        Parameters
        ----------
        figsize : Tuple[int, int]
            Figure size
        
        Returns
        -------
        plt.Figure
            Matplotlib figure
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        fig = az.plot_trace(self.trace, figsize=figsize)
        plt.tight_layout()
        
        return fig
    
    def plot_posterior(self, figsize: Tuple[int, int] = (12, 6)) -> plt.Figure:
        """
        Plot posterior distributions for all parameters.
        
        Parameters
        ----------
        figsize : Tuple[int, int]
            Figure size
        
        Returns
        -------
        plt.Figure
            Matplotlib figure
        """
        if self.trace is None:
            raise ValueError("No trace available. Run sample() first.")
        
        fig = az.plot_posterior(self.trace, figsize=figsize)
        plt.tight_layout()
        
        return fig


def detect_multiple_changepoints(data: pd.Series,
                                 n_changepoints: int = 2,
                                 model_type: str = "mean_shift",
                                 **kwargs) -> List[BayesianChangePointModel]:
    """
    Detect multiple change points sequentially.
    
    Parameters
    ----------
    data : pd.Series
        Time series data
    n_changepoints : int
        Number of change points to detect
    model_type : str
        Type of model to use
    **kwargs
        Additional arguments passed to sampling
    
    Returns
    -------
    List[BayesianChangePointModel]
        List of fitted models for each segment
    """
    logger.info(f"Detecting {n_changepoints} change points sequentially...")
    
    models = []
    remaining_data = data.copy()
    
    for i in range(n_changepoints):
        logger.info(f"\n=== Change Point {i+1}/{n_changepoints} ===")
        
        # Fit model to remaining data
        model = BayesianChangePointModel(remaining_data, name=f"CP_{i+1}")
        model.build_model(model_type=model_type)
        model.sample(**kwargs)
        
        # Get change point
        tau_idx, tau_date = model.get_change_point_estimate()
        
        # Split data at change point for next iteration
        if i < n_changepoints - 1:
            remaining_data = remaining_data.iloc[tau_idx+1:]
        
        models.append(model)
    
    return models


if __name__ == "__main__":
    # Example usage
    logger.info("Bayesian Change Point Detection Module")
    logger.info("This module provides tools for detecting structural breaks in time series data.")
