import React, { useState } from 'react';

const DateRangeFilter = ({ onDateRangeChange }) => {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const handleApply = () => {
    onDateRangeChange(startDate, endDate);
  };

  const handleReset = () => {
    setStartDate('');
    setEndDate('');
    onDateRangeChange(null, null);
  };

  const presetRanges = [
    { label: 'Last Year', days: 365 },
    { label: 'Last 3 Years', days: 1095 },
    { label: 'Last 5 Years', days: 1825 },
    { label: 'All Time', days: null },
  ];

  const handlePreset = (days) => {
    if (days === null) {
      handleReset();
      return;
    }

    const end = new Date();
    const start = new Date();
    start.setDate(start.getDate() - days);

    const startStr = start.toISOString().split('T')[0];
    const endStr = end.toISOString().split('T')[0];

    setStartDate(startStr);
    setEndDate(endStr);
    onDateRangeChange(startStr, endStr);
  };

  return (
    <div className="bg-white shadow rounded-lg p-4">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Date Range Filter</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Date Inputs */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Start Date
          </label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            End Date
          </label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        {/* Action Buttons */}
        <div className="flex items-end gap-2">
          <button
            onClick={handleApply}
            className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            Apply
          </button>
          <button
            onClick={handleReset}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500"
          >
            Reset
          </button>
        </div>

        {/* Preset Ranges */}
        <div className="flex items-end">
          <div className="w-full">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Quick Select
            </label>
            <select
              onChange={(e) => handlePreset(e.target.value === '' ? null : parseInt(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              defaultValue=""
            >
              <option value="">Select range...</option>
              {presetRanges.map((range) => (
                <option key={range.label} value={range.days}>
                  {range.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DateRangeFilter;
