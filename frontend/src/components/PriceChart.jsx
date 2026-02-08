import React, { useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';

const PriceChart = ({ data, events = [], changePoints = [] }) => {
  const [showMA, setShowMA] = useState(true);
  const [showBB, setShowBB] = useState(false);

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 border border-gray-300 rounded shadow-lg">
          <p className="font-semibold">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color }}>
              {entry.name}: ${entry.value?.toFixed(2)}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div>
      {/* Controls */}
      <div className="mb-4 flex gap-4">
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={showMA}
            onChange={(e) => setShowMA(e.target.checked)}
            className="mr-2"
          />
          <span className="text-sm">Show Moving Averages</span>
        </label>
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={showBB}
            onChange={(e) => setShowBB(e.target.checked)}
            className="mr-2"
          />
          <span className="text-sm">Show Bollinger Bands</span>
        </label>
      </div>

      {/* Chart */}
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => {
              const date = new Date(value);
              return `${date.getMonth() + 1}/${date.getFullYear()}`;
            }}
          />
          <YAxis
            label={{ value: 'Price (USD)', angle: -90, position: 'insideLeft' }}
            domain={['auto', 'auto']}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />

          {/* Bollinger Bands */}
          {showBB && (
            <>
              <Line
                type="monotone"
                dataKey="bbUpper"
                stroke="#94a3b8"
                strokeWidth={1}
                dot={false}
                name="BB Upper"
                strokeDasharray="5 5"
              />
              <Line
                type="monotone"
                dataKey="bbLower"
                stroke="#94a3b8"
                strokeWidth={1}
                dot={false}
                name="BB Lower"
                strokeDasharray="5 5"
              />
            </>
          )}

          {/* Moving Averages */}
          {showMA && (
            <>
              <Line
                type="monotone"
                dataKey="ma30"
                stroke="#f59e0b"
                strokeWidth={1.5}
                dot={false}
                name="MA 30"
              />
              <Line
                type="monotone"
                dataKey="ma60"
                stroke="#8b5cf6"
                strokeWidth={1.5}
                dot={false}
                name="MA 60"
              />
            </>
          )}

          {/* Price Line */}
          <Line
            type="monotone"
            dataKey="price"
            stroke="#0ea5e9"
            strokeWidth={2}
            dot={false}
            name="Price"
          />

          {/* Change Points */}
          {changePoints.map((cp, index) => (
            <ReferenceLine
              key={index}
              x={cp.date}
              stroke="#ef4444"
              strokeWidth={2}
              strokeDasharray="3 3"
              label={{ value: 'CP', position: 'top' }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>

      {/* Legend for events */}
      {events.length > 0 && (
        <div className="mt-4 text-sm text-gray-600">
          <p className="font-medium">Key Events:</p>
          <ul className="list-disc list-inside">
            {events.slice(0, 5).map((event, index) => (
              <li key={index}>
                {event.date}: {event.name}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default PriceChart;
