import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import ChangePointChart from '../components/ChangePointChart';

const ChangePointAnalysis = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [changePoints, setChangePoints] = useState([]);
  const [priceData, setPriceData] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [changePointsRes, historicalRes] = await Promise.all([
        apiService.getChangePoints(),
        apiService.getHistoricalData({ include_indicators: false }),
      ]);

      setChangePoints(changePointsRes.data.changepoints);

      // Transform price data
      const transformedData = Object.entries(historicalRes.data.data).map(([date, values]) => ({
        date,
        price: values.Price,
      }));

      setPriceData(transformedData);
    } catch (err) {
      console.error('Error fetching change point data:', err);
      setError('Failed to load change point data. Please ensure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="loading-spinner"></div>
        <span className="ml-3 text-gray-600">Loading change point analysis...</span>
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
          Change Point Detection Analysis
        </h2>
        <p className="text-gray-600">
          Bayesian change point detection identifies structural breaks in oil price time series
        </p>
      </div>

      {/* Change Point Visualization */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Detected Change Points
        </h3>
        <ChangePointChart data={priceData} changePoints={changePoints} />
      </div>

      {/* Change Point Details */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Change Point Details
        </h3>
        <div className="space-y-4">
          {changePoints.map((cp, index) => (
            <div
              key={index}
              className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h4 className="text-lg font-semibold text-gray-900">
                      {new Date(cp.date).toLocaleDateString('en-US', {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric',
                      })}
                    </h4>
                    <span className="px-3 py-1 bg-primary-100 text-primary-800 text-sm font-medium rounded-full">
                      Confidence: {(cp.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                  <p className="text-gray-700 mb-3">{cp.description}</p>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-gray-50 p-3 rounded">
                      <p className="text-xs text-gray-600 mb-1">Mean Before</p>
                      <p className="text-lg font-semibold text-gray-900">
                        ${cp.mean_before.toFixed(2)}
                      </p>
                    </div>
                    <div className="bg-gray-50 p-3 rounded">
                      <p className="text-xs text-gray-600 mb-1">Mean After</p>
                      <p className="text-lg font-semibold text-gray-900">
                        ${cp.mean_after.toFixed(2)}
                      </p>
                    </div>
                    <div className="bg-gray-50 p-3 rounded">
                      <p className="text-xs text-gray-600 mb-1">Change</p>
                      <p
                        className={`text-lg font-semibold ${
                          cp.mean_after > cp.mean_before
                            ? 'text-green-600'
                            : 'text-red-600'
                        }`}
                      >
                        {cp.mean_after > cp.mean_before ? '+' : ''}
                        {((cp.mean_after - cp.mean_before) / cp.mean_before * 100).toFixed(1)}%
                      </p>
                    </div>
                  </div>
                  <p className="mt-3 text-sm text-gray-600 italic">{cp.impact}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Methodology */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-2">
          About Change Point Detection
        </h3>
        <p className="text-sm text-blue-800">
          Change point detection uses Bayesian statistical methods to identify significant
          structural breaks in the time series. These points represent moments where the
          underlying statistical properties of the data (such as mean or variance) change
          significantly, often corresponding to major economic or geopolitical events.
        </p>
      </div>
    </div>
  );
};

export default ChangePointAnalysis;
