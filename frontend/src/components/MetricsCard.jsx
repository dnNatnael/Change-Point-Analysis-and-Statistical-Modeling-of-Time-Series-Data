import React from 'react';

const MetricsCard = ({ title, value, subtitle, trend, trendValue }) => {
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg card-hover">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-1">
            <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
            <dd className="mt-1 text-3xl font-semibold text-gray-900">{value}</dd>
            {subtitle && (
              <p className="mt-1 text-sm text-gray-600">{subtitle}</p>
            )}
            {trend && trendValue && (
              <div className="mt-2 flex items-center">
                <span
                  className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    trend === 'up'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  }`}
                >
                  {trend === 'up' ? '↑' : '↓'} {trendValue}
                </span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MetricsCard;
