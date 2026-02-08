"""
Flask Backend API for Brent Oil Price Analysis Dashboard
=========================================================
Provides RESTful API endpoints for serving analysis results to the frontend.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import sys
import os
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import load_brent_data, load_events_data, compute_log_returns
from src.time_series_analysis import (
    compute_volatility, 
    detect_volatility_regimes,
    compute_rolling_statistics
)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
DATA_PATH = Path(__file__).parent.parent / 'data' / 'raw' / 'BrentOilPrices.csv'
EVENTS_PATH = Path(__file__).parent.parent / 'references' / 'geopolitical_events.csv'

# Cache for loaded data
_data_cache = {}


def get_price_data():
    """Load and cache price data."""
    if 'price_data' not in _data_cache:
        df = load_brent_data(str(DATA_PATH))
        df = compute_log_returns(df)
        df = compute_volatility(df, windows=[30, 60, 90])
        df = detect_volatility_regimes(df)
        df = compute_rolling_statistics(df)
        _data_cache['price_data'] = df
    return _data_cache['price_data']


def get_events_data():
    """Load and cache events data."""
    if 'events_data' not in _data_cache:
        df = load_events_data(str(EVENTS_PATH))
        _data_cache['events_data'] = df
    return _data_cache['events_data']


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/data/historical', methods=['GET'])
def get_historical_data():
    """
    Get historical price data with optional date filtering.
    
    Query Parameters:
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    - include_indicators: Include technical indicators (true/false)
    """
    try:
        df = get_price_data()
        
        # Parse query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        include_indicators = request.args.get('include_indicators', 'false').lower() == 'true'
        
        # Filter by date range
        if start_date:
            df = df[df.index >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df.index <= pd.to_datetime(end_date)]
        
        # Select columns
        if include_indicators:
            columns = ['Price', 'Log_Returns', 'Volatility_30d', 'Volatility_60d', 
                      'Volatility_90d', 'Avg_Volatility', 'Volatility_Regime',
                      'MA_30', 'MA_60', 'BB_Upper', 'BB_Middle', 'BB_Lower']
        else:
            columns = ['Price', 'Log_Returns']
        
        # Prepare response
        result = df[columns].copy()
        result.index = result.index.strftime('%Y-%m-%d')
        
        return jsonify({
            'data': result.to_dict(orient='index'),
            'count': len(result),
            'start_date': result.index[0] if len(result) > 0 else None,
            'end_date': result.index[-1] if len(result) > 0 else None
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/data/summary', methods=['GET'])
def get_data_summary():
    """Get summary statistics for the price data."""
    try:
        df = get_price_data()
        
        summary = {
            'total_records': len(df),
            'date_range': {
                'start': df.index.min().strftime('%Y-%m-%d'),
                'end': df.index.max().strftime('%Y-%m-%d')
            },
            'price_stats': {
                'mean': float(df['Price'].mean()),
                'median': float(df['Price'].median()),
                'std': float(df['Price'].std()),
                'min': float(df['Price'].min()),
                'max': float(df['Price'].max()),
                'current': float(df['Price'].iloc[-1])
            },
            'volatility_stats': {
                'avg_volatility': float(df['Avg_Volatility'].mean()),
                'max_volatility': float(df['Avg_Volatility'].max()),
                'min_volatility': float(df['Avg_Volatility'].min())
            },
            'regime_distribution': df['Volatility_Regime'].value_counts().to_dict()
        }
        
        return jsonify(summary)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/events', methods=['GET'])
def get_events():
    """
    Get geopolitical events data with optional filtering.
    
    Query Parameters:
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    - event_type: Filter by event type
    """
    try:
        df = get_events_data()
        
        # Parse query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        event_type = request.args.get('event_type')
        
        # Filter by date range
        if start_date:
            df = df[df.index >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df.index <= pd.to_datetime(end_date)]
        
        # Filter by event type
        if event_type and 'Event_Type' in df.columns:
            df = df[df['Event_Type'] == event_type]
        
        # Prepare response
        result = df.copy()
        result.index = result.index.strftime('%Y-%m-%d')
        
        return jsonify({
            'events': result.to_dict(orient='index'),
            'count': len(result)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/events/types', methods=['GET'])
def get_event_types():
    """Get list of unique event types."""
    try:
        df = get_events_data()
        
        if 'Event_Type' in df.columns:
            event_types = df['Event_Type'].unique().tolist()
        else:
            event_types = []
        
        return jsonify({
            'event_types': event_types,
            'count': len(event_types)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analysis/correlation', methods=['GET'])
def get_event_correlation():
    """
    Analyze correlation between events and price changes.
    
    Query Parameters:
    - window_days: Number of days before/after event to analyze (default: 30)
    """
    try:
        price_df = get_price_data()
        events_df = get_events_data()
        
        window_days = int(request.args.get('window_days', 30))
        
        correlations = []
        
        for event_date, event_row in events_df.iterrows():
            # Get price data around event
            start_date = event_date - pd.Timedelta(days=window_days)
            end_date = event_date + pd.Timedelta(days=window_days)
            
            window_data = price_df[(price_df.index >= start_date) & 
                                   (price_df.index <= end_date)]
            
            if len(window_data) > 0:
                # Calculate price change
                price_before = window_data[window_data.index < event_date]['Price'].mean()
                price_after = window_data[window_data.index >= event_date]['Price'].mean()
                
                if pd.notna(price_before) and pd.notna(price_after):
                    price_change = ((price_after - price_before) / price_before) * 100
                    
                    # Calculate volatility change
                    vol_before = window_data[window_data.index < event_date]['Avg_Volatility'].mean()
                    vol_after = window_data[window_data.index >= event_date]['Avg_Volatility'].mean()
                    
                    correlations.append({
                        'event_date': event_date.strftime('%Y-%m-%d'),
                        'event': event_row.get('Event', 'Unknown'),
                        'event_type': event_row.get('Event_Type', 'Unknown'),
                        'expected_impact': event_row.get('Expected_Impact', 'Unknown'),
                        'price_change_pct': float(price_change),
                        'price_before': float(price_before),
                        'price_after': float(price_after),
                        'volatility_before': float(vol_before) if pd.notna(vol_before) else None,
                        'volatility_after': float(vol_after) if pd.notna(vol_after) else None
                    })
        
        return jsonify({
            'correlations': correlations,
            'count': len(correlations),
            'window_days': window_days
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analysis/volatility', methods=['GET'])
def get_volatility_analysis():
    """Get volatility analysis over time."""
    try:
        df = get_price_data()
        
        # Parse query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Filter by date range
        if start_date:
            df = df[df.index >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df.index <= pd.to_datetime(end_date)]
        
        # Prepare volatility data
        vol_data = df[['Volatility_30d', 'Volatility_60d', 'Volatility_90d', 
                       'Avg_Volatility', 'Volatility_Regime']].copy()
        vol_data.index = vol_data.index.strftime('%Y-%m-%d')
        
        return jsonify({
            'data': vol_data.to_dict(orient='index'),
            'count': len(vol_data)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analysis/changepoints', methods=['GET'])
def get_changepoints():
    """
    Get detected change points from analysis.
    Note: This is a placeholder - actual change point detection would be run separately.
    """
    try:
        # This would typically load pre-computed change point results
        # For now, return a sample structure
        changepoints = [
            {
                'date': '2008-09-15',
                'description': 'Financial Crisis - Lehman Brothers Collapse',
                'confidence': 0.95,
                'mean_before': 95.5,
                'mean_after': 45.2,
                'impact': 'Major decrease in price levels'
            },
            {
                'date': '2014-11-27',
                'description': 'OPEC No Cut Decision - Oil Price Crash',
                'confidence': 0.92,
                'mean_before': 85.3,
                'mean_after': 52.1,
                'impact': 'Significant price decline'
            }
        ]
        
        return jsonify({
            'changepoints': changepoints,
            'count': len(changepoints)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analysis/metrics', methods=['GET'])
def get_performance_metrics():
    """Get model performance metrics."""
    try:
        df = get_price_data()
        
        # Calculate various metrics
        returns = df['Log_Returns'].dropna()
        
        metrics = {
            'returns': {
                'mean_daily': float(returns.mean()),
                'std_daily': float(returns.std()),
                'annualized_return': float(returns.mean() * 252),
                'annualized_volatility': float(returns.std() * np.sqrt(252)),
                'sharpe_ratio': float((returns.mean() * 252) / (returns.std() * np.sqrt(252)))
            },
            'price': {
                'total_return': float((df['Price'].iloc[-1] / df['Price'].iloc[0] - 1) * 100),
                'max_drawdown': float(((df['Price'] / df['Price'].cummax() - 1).min()) * 100),
                'current_price': float(df['Price'].iloc[-1])
            },
            'volatility': {
                'current': float(df['Avg_Volatility'].iloc[-1]),
                'average': float(df['Avg_Volatility'].mean()),
                'max': float(df['Avg_Volatility'].max()),
                'min': float(df['Avg_Volatility'].min())
            }
        }
        
        return jsonify(metrics)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Starting Flask API server...")
    print(f"Data path: {DATA_PATH}")
    print(f"Events path: {EVENTS_PATH}")
    app.run(debug=True, host='0.0.0.0', port=5000)
