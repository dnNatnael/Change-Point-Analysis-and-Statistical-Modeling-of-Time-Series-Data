# Brent Oil Price Analysis Dashboard

An interactive web application for visualizing and analyzing Brent crude oil price data, featuring change point detection, event correlation analysis, and comprehensive time series visualizations.

## 🎯 Features

### Backend (Flask)
- **RESTful API** with documented endpoints
- **Historical Price Data** serving with optional date filtering
- **Event Correlation Analysis** showing how geopolitical events affect prices
- **Change Point Detection** results from Bayesian analysis
- **Performance Metrics** including volatility, returns, and risk measures
- **Data Caching** for improved performance

### Frontend (React)
- **Interactive Dashboard** with real-time data visualization
- **Multiple Chart Types** using Recharts library:
  - Line charts for price trends
  - Area charts for volatility analysis
  - Bar charts for event impact correlation
- **Date Range Filters** with preset options
- **Event Timeline** with expandable details
- **Responsive Design** for desktop, tablet, and mobile devices
- **Event Highlighting** to visualize price spikes/drops
- **Drill-down Capability** for deeper insights

## 📋 Prerequisites

### Backend Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Frontend Requirements
- Node.js 16.x or higher
- npm or yarn package manager

## 🚀 Installation & Setup

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

The backend API will be available at `http://localhost:5000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend application will be available at `http://localhost:3000`

## 📁 Project Structure

```
.
├── backend/
│   ├── app.py                 # Flask application with API endpoints
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── PriceChart.jsx
│   │   │   ├── VolatilityChart.jsx
│   │   │   ├── EventCorrelationChart.jsx
│   │   │   ├── EventTimeline.jsx
│   │   │   ├── ChangePointChart.jsx
│   │   │   ├── MetricsCard.jsx
│   │   │   └── DateRangeFilter.jsx
│   │   ├── pages/             # Page components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── EventAnalysis.jsx
│   │   │   └── ChangePointAnalysis.jsx
│   │   ├── services/          # API service layer
│   │   │   └── api.js
│   │   ├── App.jsx            # Main application component
│   │   ├── main.jsx           # Application entry point
│   │   └── index.css          # Global styles
│   ├── package.json           # Node dependencies
│   ├── vite.config.js         # Vite configuration
│   └── tailwind.config.js     # Tailwind CSS configuration
│
├── src/                       # Analysis modules
│   ├── data_loader.py
│   ├── bayesian_changepoint.py
│   ├── time_series_analysis.py
│   └── visualization.py
│
├── data/
│   └── raw/
│       └── BrentOilPrices.csv
│
└── references/
    └── geopolitical_events.csv
```

## 🔌 API Endpoints

### Health Check
- `GET /api/health` - Check API status

### Data Endpoints
- `GET /api/data/historical` - Get historical price data
  - Query params: `start_date`, `end_date`, `include_indicators`
- `GET /api/data/summary` - Get data summary statistics

### Event Endpoints
- `GET /api/events` - Get geopolitical events
  - Query params: `start_date`, `end_date`, `event_type`
- `GET /api/events/types` - Get list of event types

### Analysis Endpoints
- `GET /api/analysis/correlation` - Get event-price correlations
  - Query params: `window_days`
- `GET /api/analysis/volatility` - Get volatility analysis
  - Query params: `start_date`, `end_date`
- `GET /api/analysis/changepoints` - Get detected change points
- `GET /api/analysis/metrics` - Get performance metrics

## 📊 Dashboard Pages

### 1. Main Dashboard
- **Overview metrics** (current price, average, volatility, Sharpe ratio)
- **Historical price chart** with moving averages and Bollinger Bands
- **Volatility analysis** over time
- **Data summary** with regime distribution

### 2. Event Analysis
- **Event impact visualization** showing price changes around events
- **Event timeline** with expandable details
- **Event type filtering** (Geopolitical, Economic, Policy, etc.)
- **Configurable analysis window** (7-90 days)

### 3. Change Point Analysis
- **Detected change points** visualization on price chart
- **Detailed change point information** with confidence levels
- **Before/after statistics** for each change point
- **Impact assessment** of structural breaks

## 🎨 Key Features Explained

### Date Range Filtering
- Custom date range selection
- Preset options (Last Year, 3 Years, 5 Years, All Time)
- Real-time chart updates

### Event Highlighting
- Visual markers on price charts for major events
- Color-coded event types
- Hover tooltips with event details

### Interactive Charts
- Zoom and pan capabilities
- Toggle chart elements (MA, Bollinger Bands)
- Responsive tooltips with detailed information
- Export-ready visualizations

### Responsive Design
- Mobile-first approach
- Adaptive layouts for all screen sizes
- Touch-friendly interactions
- Optimized performance

## 🔧 Configuration

### Backend Configuration
Edit [`backend/app.py`](backend/app.py:1) to modify:
- Data file paths
- API port (default: 5000)
- CORS settings

### Frontend Configuration
Edit [`frontend/vite.config.js`](frontend/vite.config.js:1) to modify:
- Development server port (default: 3000)
- API proxy settings

Create a `.env` file in the frontend directory:
```env
VITE_API_URL=http://localhost:5000/api
```

## 📈 Data Requirements

### Price Data Format (CSV)
```csv
Date,Price
2020-01-01,66.00
2020-01-02,66.25
...
```

### Events Data Format (CSV)
```csv
Event_Date,Event,Event_Type,Description,Expected_Impact
2020-03-09,Oil Price War,Geopolitical,Saudi-Russia price war,Price decrease
...
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
# Test API health
curl http://localhost:5000/api/health

# Test data endpoint
curl http://localhost:5000/api/data/summary
```

### Frontend Testing
```bash
cd frontend
# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🚀 Production Deployment

### Backend Deployment
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend Deployment
```bash
# Build for production
npm run build

# The dist/ folder contains the production build
# Deploy to any static hosting service (Netlify, Vercel, etc.)
```

## 📝 Usage Examples

### Analyzing Event Impact
1. Navigate to the **Event Analysis** page
2. Select an event type filter (e.g., "Geopolitical")
3. Adjust the analysis window (e.g., 30 days)
4. View the correlation chart showing price changes
5. Expand events in the timeline for detailed information

### Exploring Change Points
1. Navigate to the **Change Point Analysis** page
2. View detected structural breaks on the price chart
3. Review detailed statistics for each change point
4. Compare mean prices before and after each break

### Custom Date Range Analysis
1. On the main dashboard, use the date range filter
2. Select a custom start and end date
3. Or choose a preset range (e.g., "Last 3 Years")
4. Click "Apply" to update all visualizations

## 🛠️ Troubleshooting

### Backend Issues
- **Port already in use**: Change port in `app.py` or kill the process using port 5000
- **Module not found**: Ensure virtual environment is activated and dependencies are installed
- **Data file not found**: Check file paths in `app.py` match your data location

### Frontend Issues
- **API connection failed**: Ensure backend is running on port 5000
- **Build errors**: Delete `node_modules` and run `npm install` again
- **Blank page**: Check browser console for errors and ensure API is accessible

## 📚 Technologies Used

### Backend
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing

### Frontend
- **React** - UI library
- **Vite** - Build tool
- **Recharts** - Charting library
- **Tailwind CSS** - Styling framework
- **Axios** - HTTP client
- **React Router** - Navigation

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the Brent Oil Price Analysis research project.

## 👥 Authors

10 Academy - Data Analysis Team

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review API documentation
- Contact the development team

---

**Note**: Ensure both backend and frontend servers are running simultaneously for full functionality.
