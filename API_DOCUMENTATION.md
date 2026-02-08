# Brent Oil Analysis Dashboard - API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, no authentication is required for API endpoints.

---

## Endpoints

### Health Check

#### `GET /health`
Check if the API server is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

---

### Historical Data

#### `GET /data/historical`
Retrieve historical Brent oil price data with optional technical indicators.

**Query Parameters:**
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `include_indicators` (optional): Include technical indicators (true/false, default: false)

**Example Request:**
```
GET /data/historical?start_date=2020-01-01&end_date=2023-12-31&include_indicators=true
```

**Response:**
```json
{
  "data": {
    "2020-01-01": {
      "Price": 66.00,
      "Log_Returns": 0.0015,
      "Volatility_30d": 0.25,
      "Volatility_60d": 0.23,
      "Volatility_90d": 0.24,
      "Avg_Volatility": 0.24,
      "Volatility_Regime": "Medium",
      "MA_30": 65.50,
      "MA_60": 64.80,
      "BB_Upper": 68.00,
      "BB_Middle": 66.00,
      "BB_Lower": 64.00
    },
    ...
  },
  "count": 1461,
  "start_date": "2020-01-01",
  "end_date": "2023-12-31"
}
```

---

#### `GET /data/summary`
Get summary statistics for the entire price dataset.

**Response:**
```json
{
  "total_records": 10000,
  "date_range": {
    "start": "1987-05-20",
    "end": "2024-01-15"
  },
  "price_stats": {
    "mean": 55.32,
    "median": 52.10,
    "std": 28.45,
    "min": 9.82,
    "max": 147.27,
    "current": 78.50
  },
  "volatility_stats": {
    "avg_volatility": 0.35,
    "max_volatility": 1.25,
    "min_volatility": 0.08
  },
  "regime_distribution": {
    "Low": 3245,
    "Medium": 3567,
    "High": 3188
  }
}
```

---

### Events

#### `GET /events`
Retrieve geopolitical events data with optional filtering.

**Query Parameters:**
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `event_type` (optional): Filter by event type (e.g., "Geopolitical", "Economic")

**Example Request:**
```
GET /events?start_date=2020-01-01&event_type=Geopolitical
```

**Response:**
```json
{
  "events": {
    "2020-03-09": {
      "Event": "Oil Price War",
      "Event_Type": "Geopolitical",
      "Description": "Saudi-Russia price war begins",
      "Expected_Impact": "Supply increase - Price decrease"
    },
    ...
  },
  "count": 45
}
```

---

#### `GET /events/types`
Get list of unique event types.

**Response:**
```json
{
  "event_types": [
    "Geopolitical",
    "Economic",
    "Policy",
    "Military",
    "Supply",
    "Market",
    "Natural"
  ],
  "count": 7
}
```

---

### Analysis

#### `GET /analysis/correlation`
Analyze correlation between events and price changes.

**Query Parameters:**
- `window_days` (optional): Number of days before/after event to analyze (default: 30)

**Example Request:**
```
GET /analysis/correlation?window_days=30
```

**Response:**
```json
{
  "correlations": [
    {
      "event_date": "2008-09-15",
      "event": "Lehman Brothers Collapse",
      "event_type": "Economic",
      "expected_impact": "Demand collapse - Price crash",
      "price_change_pct": -35.5,
      "price_before": 95.50,
      "price_after": 61.60,
      "volatility_before": 0.45,
      "volatility_after": 0.85
    },
    ...
  ],
  "count": 50,
  "window_days": 30
}
```

---

#### `GET /analysis/volatility`
Get volatility analysis over time.

**Query Parameters:**
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format

**Example Request:**
```
GET /analysis/volatility?start_date=2020-01-01
```

**Response:**
```json
{
  "data": {
    "2020-01-01": {
      "Volatility_30d": 0.25,
      "Volatility_60d": 0.23,
      "Volatility_90d": 0.24,
      "Avg_Volatility": 0.24,
      "Volatility_Regime": "Medium"
    },
    ...
  },
  "count": 1461
}
```

---

#### `GET /analysis/changepoints`
Get detected change points from Bayesian analysis.

**Response:**
```json
{
  "changepoints": [
    {
      "date": "2008-09-15",
      "description": "Financial Crisis - Lehman Brothers Collapse",
      "confidence": 0.95,
      "mean_before": 95.5,
      "mean_after": 45.2,
      "impact": "Major decrease in price levels"
    },
    {
      "date": "2014-11-27",
      "description": "OPEC No Cut Decision - Oil Price Crash",
      "confidence": 0.92,
      "mean_before": 85.3,
      "mean_after": 52.1,
      "impact": "Significant price decline"
    }
  ],
  "count": 2
}
```

---

#### `GET /analysis/metrics`
Get comprehensive performance metrics.

**Response:**
```json
{
  "returns": {
    "mean_daily": 0.0002,
    "std_daily": 0.025,
    "annualized_return": 0.05,
    "annualized_volatility": 0.40,
    "sharpe_ratio": 0.125
  },
  "price": {
    "total_return": 45.5,
    "max_drawdown": -65.2,
    "current_price": 78.50
  },
  "volatility": {
    "current": 0.32,
    "average": 0.35,
    "max": 1.25,
    "min": 0.08
  }
}
```

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "error": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**
- `200 OK`: Request successful
- `400 Bad Request`: Invalid parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing rate limiting.

---

## CORS

CORS is enabled for all origins. In production, configure specific allowed origins.

---

## Data Formats

### Date Format
All dates use ISO 8601 format: `YYYY-MM-DD`

### Number Precision
- Prices: 2 decimal places
- Returns: 4 decimal places
- Volatility: 2-4 decimal places
- Percentages: 2 decimal places

---

## Usage Examples

### Python
```python
import requests

# Get historical data
response = requests.get(
    'http://localhost:5000/api/data/historical',
    params={
        'start_date': '2020-01-01',
        'include_indicators': 'true'
    }
)
data = response.json()
```

### JavaScript
```javascript
// Get event correlation
fetch('http://localhost:5000/api/analysis/correlation?window_days=30')
  .then(response => response.json())
  .then(data => console.log(data));
```

### cURL
```bash
# Get data summary
curl http://localhost:5000/api/data/summary

# Get events by type
curl "http://localhost:5000/api/events?event_type=Economic"
```

---

## Notes

1. **Data Caching**: The API caches loaded data for improved performance. Restart the server to reload data.

2. **Date Filtering**: When using date filters, ensure dates are within the available data range.

3. **Performance**: Large date ranges may take longer to process. Consider using pagination for production use.

4. **Data Updates**: To update the underlying data, modify the CSV files and restart the server.

---

## Support

For issues or questions about the API, refer to the main README or contact the development team.
