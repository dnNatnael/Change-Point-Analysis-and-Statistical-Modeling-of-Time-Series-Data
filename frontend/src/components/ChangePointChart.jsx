import React from 'react';
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
  ReferenceArea,
} from 'recharts';

const ChangePointChart = ({ data, changePoints }) => {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 border border-gray-300 rounded shadow-lg">
          <p className="font-semibold">{label}</p>
          <p style={{ color: payload[0].color }}>
            Price: ${payload[0].value?.toFixed(2)}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div>
      <div className="mb-4">
        <p className="text-sm text-gray-600">
          Red vertical lines indicate detected change points where significant structural
          breaks occurred in the price series.
        </p>
      </div>

      <ResponsiveContainer width="100%" height={450}>
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
              strokeDasharray="5 5"
              label={{
                value: `CP ${index + 1}`,
                position: 'top',
                fill: '#ef4444',
                fontSize: 12,
              }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>

      {/* Change Point Legend */}
      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
        {changePoints.map((cp, index) => (
          <div
            key={index}
            className="flex items-center gap-2 text-xs bg-red-50 p-2 rounded"
          >
            <span className="font-semibold text-red-600">CP {index + 1}:</span>
            <span className="text-gray-700">
              {new Date(cp.date).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
              })}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChangePointChart;
