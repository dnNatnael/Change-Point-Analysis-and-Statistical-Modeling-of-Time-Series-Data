import React, { useState } from 'react';

const EventTimeline = ({ events }) => {
  const [expandedEvent, setExpandedEvent] = useState(null);

  const getEventTypeColor = (type) => {
    const colors = {
      Geopolitical: 'bg-red-100 text-red-800 border-red-300',
      Military: 'bg-orange-100 text-orange-800 border-orange-300',
      Economic: 'bg-blue-100 text-blue-800 border-blue-300',
      Policy: 'bg-purple-100 text-purple-800 border-purple-300',
      Supply: 'bg-green-100 text-green-800 border-green-300',
      Market: 'bg-yellow-100 text-yellow-800 border-yellow-300',
      Natural: 'bg-gray-100 text-gray-800 border-gray-300',
    };
    return colors[type] || 'bg-gray-100 text-gray-800 border-gray-300';
  };

  const sortedEvents = [...events].sort((a, b) => new Date(b.date) - new Date(a.date));

  return (
    <div className="space-y-4 max-h-96 overflow-y-auto">
      {sortedEvents.map((event, index) => (
        <div
          key={index}
          className="border-l-4 border-primary-500 pl-4 py-2 hover:bg-gray-50 cursor-pointer transition-colors"
          onClick={() => setExpandedEvent(expandedEvent === index ? null : index)}
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-sm font-semibold text-gray-900">
                  {new Date(event.date).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                  })}
                </span>
                <span
                  className={`px-2 py-0.5 text-xs font-medium rounded border ${getEventTypeColor(
                    event.Event_Type
                  )}`}
                >
                  {event.Event_Type}
                </span>
              </div>
              <h4 className="text-sm font-medium text-gray-900">{event.Event}</h4>
              {expandedEvent === index && (
                <div className="mt-2 text-sm text-gray-600 space-y-1">
                  {event.Description && <p>{event.Description}</p>}
                  {event.Expected_Impact && (
                    <p className="text-xs italic">
                      <span className="font-medium">Expected Impact:</span>{' '}
                      {event.Expected_Impact}
                    </p>
                  )}
                </div>
              )}
            </div>
            <button className="text-gray-400 hover:text-gray-600">
              {expandedEvent === index ? '▼' : '▶'}
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default EventTimeline;
