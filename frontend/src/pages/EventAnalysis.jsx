import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import EventCorrelationChart from '../components/EventCorrelationChart';
import EventTimeline from '../components/EventTimeline';

const EventAnalysis = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [events, setEvents] = useState([]);
  const [correlations, setCorrelations] = useState([]);
  const [eventTypes, setEventTypes] = useState([]);
  const [selectedType, setSelectedType] = useState('');
  const [windowDays, setWindowDays] = useState(30);

  useEffect(() => {
    fetchData();
  }, [selectedType, windowDays]);

  const fetchData = async () => {
    try {
      setLoading(true);
      setError(null);

      const params = {
        ...(selectedType && { event_type: selectedType }),
      };

      const [eventsRes, correlationsRes, typesRes] = await Promise.all([
        apiService.getEvents(params),
        apiService.getEventCorrelation({ window_days: windowDays }),
        apiService.getEventTypes(),
      ]);

      const eventsArray = Object.entries(eventsRes.data.events).map(([date, event]) => ({
        date,
        ...event,
      }));

      setEvents(eventsArray);
      setCorrelations(correlationsRes.data.correlations);
      setEventTypes(typesRes.data.event_types);
    } catch (err) {
      console.error('Error fetching event data:', err);
      setError('Failed to load event data. Please ensure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="loading-spinner"></div>
        <span className="ml-3 text-gray-600">Loading event analysis...</span>
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
          Event Impact Analysis
        </h2>
        <p className="text-gray-600">
          Analyze how geopolitical events correlate with Brent oil price changes
        </p>
      </div>

      {/* Filters */}
      <div className="bg-white shadow rounded-lg p-4">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Filters</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Event Type
            </label>
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">All Types</option>
              {eventTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Analysis Window (days)
            </label>
            <select
              value={windowDays}
              onChange={(e) => setWindowDays(parseInt(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="7">7 days</option>
              <option value="14">14 days</option>
              <option value="30">30 days</option>
              <option value="60">60 days</option>
              <option value="90">90 days</option>
            </select>
          </div>
        </div>
      </div>

      {/* Event Correlation Chart */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Event Impact on Prices
        </h3>
        <EventCorrelationChart data={correlations} />
      </div>

      {/* Event Timeline */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Event Timeline
        </h3>
        <EventTimeline events={events} />
      </div>

      {/* Event Statistics */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-xl font-semibold text-gray-900 mb-4">
          Event Statistics
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">Total Events</p>
            <p className="text-2xl font-bold text-blue-600">{events.length}</p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">Positive Impact</p>
            <p className="text-2xl font-bold text-green-600">
              {correlations.filter((c) => c.price_change_pct > 0).length}
            </p>
          </div>
          <div className="bg-red-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">Negative Impact</p>
            <p className="text-2xl font-bold text-red-600">
              {correlations.filter((c) => c.price_change_pct < 0).length}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventAnalysis;
