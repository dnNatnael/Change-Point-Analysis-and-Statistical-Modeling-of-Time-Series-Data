import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import PriceChart from '../components/PriceChart';
import VolatilityChart from '../components/VolatilityChart';
import MetricsCard from '../components/MetricsCard';
import DateRangeFilter from '../components/DateRangeFilter';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [priceData, setPriceData] = useState([]);
  const [summary, setSummary] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [dateRange, setDateRange] = useState({ start: null, end: null });

  useEffect(() => {
    fetchData();
  }, [dateRange]);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      const params = {
        include_indicators: true,
        ...(dateRange.start && { start_date: dateRange.start }),
        ...(dateRange.end && { end_date: dateRange.end }),
      };

      const [historicalRes, summaryRes, metricsRes] = await Promise.all([
        apiService.getHistoricalData(params),
        apiService.getDataSummary(),
        apiService.getPerformanceMetrics(),
      ]);

      // Transform data for charts
      const transformedData = Object.entries(historicalRes.data.data).map(([date, values]) => ({
        date,
        price: values.Price,
        returns: values.Log_Returns,
        volatility: values.Avg_Volatility,
        ma30: values.MA_30,
        ma60: values.MA_60,
        bbUpper: values.BB_Upper,
        bbMiddle: values.BB_Middle,
        bbLower: values.BB_Lower,
      }));

      setPriceData(transformedData);
      setSummary(summaryRes.data);
      setMetrics(metricsRes.data);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to load data. Please ensure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleDateRangeChange = (start, end) => {
    setDateRange({ start, end });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="loading-spinner"></div>
        <span className="ml-3 text-gray-600">Loading dashboard data...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">{error}</p>
        <button
          onClick={fetchData}
          className="mt-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          Brent Oil Price Analysis Dashboard
        </h2>
        <p className="text-gray-600">
          Interactive visualization of historical Brent crude oil prices and analysis results
        </p>
      </div>

      {/* Date Range Filter */}
      <DateRangeFilter onDateRangeChange={handleDateRangeChange} />

      {/* Metrics Cards */}
      {summary && metrics && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricsCard
            title="Current Price"
            value={`$${summary.price_stats.current.toFixed(2)}`}
            subtitle="Per Barrel"
            trend={metrics.price.total_return > 0 ? 'up' : 'down'}
            trendValue={`${metrics.price.total_return.toFixed(2)}%`}
          />
          <MetricsCard
            title="Average Price"
            value={`$${summary.price_stats.mean.toFixed(2)}`}
            subtitle={`Range: $${summary.price_stats.min.toFixed(0)} - $${summary.price_stats.max.toFixed(0)}`}
          />
          <MetricsCard
            title="Volatility"
            value={metrics.volatility.current.toFixed(2)}
            subtitle={`Avg: ${metrics.volatility.average.toFixed(2)}`}
          />
          <MetricsCard
            title="Sharpe Ratio"
            value={metrics.returns.sharpe_ratio.toFixed(3)}
            subtitle="Risk-Adjusted Return"
          />
        </div>
      )}

      {/* Price Chart */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Historical Price Trends
        </h3>
        <PriceChart data={priceData} />
      </div>

      {/* Volatility Chart */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Volatility Analysis
        </h3>
        <VolatilityChart data={priceData} />
      </div>

      {/* Summary Statistics */}
      {summary && (
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            Data Summary
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Dataset Information</h4>
              <dl className="space-y-2">
                <div className="flex justify-between">
                  <dt className="text-gray-600">Total Records:</dt>
                  <dd className="font-medium">{summary.total_records.toLocaleString()}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="text-gray-600">Date Range:</dt>
                  <dd className="font-medium">
                    {summary.date_range.start} to {summary.date_range.end}
                  </dd>
                </div>
              </dl>
            </div>
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Volatility Regimes</h4>
              <dl className="space-y-2">
                {Object.entries(summary.regime_distribution).map(([regime, count]) => (
                  <div key={regime} className="flex justify-between">
                    <dt className="text-gray-600">{regime}:</dt>
                    <dd className="font-medium">{count.toLocaleString()} days</dd>
                  </div>
                ))}
              </dl>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
