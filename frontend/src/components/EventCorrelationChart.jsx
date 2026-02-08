import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
  ReferenceLine,
} from 'recharts';

const EventCorrelationChart = ({ data }) => {
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-4 border border-gray-300 rounded shadow-lg max-w-sm">
          <p className="font-semibold text-sm">{data.event}</p>
          <p className="text-xs text-gray-600 mb-2">{data.event_date}</p>
          <p className="text-xs">
            <span className="font-medium">Type:</span> {data.event_type}
          </p>
          <p className="text-xs">
            <span className="font-medium">Price Change:</span>{' '}
            <span
              className={
                data.price_change_pct > 0 ? 'text-green-600' : 'text-red-600'
              }
            >
              {data.price_change_pct.toFixed(2)}%
            </span>
          </p>
          <p className="text-xs">
            <span className="font-medium">Expected:</span> {data.expected_impact}
          </p>
        </div>
      );
    }
    return null;
  };

  // Sort by absolute price change
  const sortedData = [...data].sort(
    (a, b) => Math.abs(b.price_change_pct) - Math.abs(a.price_change_pct)
  ).slice(0, 20); // Show top 20 events

  return (
    <div>
      <p className="text-sm text-gray-600 mb-4">
        Showing top 20 events by price impact (% change within analysis window)
      </p>
      <ResponsiveContainer width="100%" height={500}>
        <BarChart
          data={sortedData}
          margin={{ top: 20, right: 30, left: 20, bottom: 100 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="event"
            angle={-45}
            textAnchor="end"
            height={150}
            tick={{ fontSize: 10 }}
            interval={0}
          />
          <YAxis label={{ value: 'Price Change (%)', angle: -90, position: 'insideLeft' }} />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <ReferenceLine y={0} stroke="#000" />
          <Bar dataKey="price_change_pct" name="Price Change (%)">
            {sortedData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={entry.price_change_pct > 0 ? '#10b981' : '#ef4444'}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default EventCorrelationChart;
