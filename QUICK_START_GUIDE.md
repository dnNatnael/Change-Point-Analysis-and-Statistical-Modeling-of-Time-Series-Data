# Quick Start Guide - Brent Oil Analysis Dashboard

## 🚀 Get Started in 5 Minutes

### Prerequisites Check
Before starting, ensure you have:
- ✅ Python 3.8+ installed (`python --version`)
- ✅ Node.js 16+ installed (`node --version`)
- ✅ npm installed (`npm --version`)

---

## Option 1: Automated Start (Recommended)

### Linux/Mac
```bash
chmod +x start_dashboard.sh
./start_dashboard.sh
```

### Windows
```bash
start_dashboard.bat
```

**That's it!** The script will:
1. Create virtual environments
2. Install all dependencies
3. Start both servers
4. Open the dashboard at http://localhost:3000

---

## Option 2: Manual Start

### Step 1: Start Backend (Terminal 1)
```bash
cd backend
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python app.py
```

✅ Backend running at: http://localhost:5000

### Step 2: Start Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```

✅ Frontend running at: http://localhost:3000

---

## 🎯 First Steps in the Dashboard

### 1. Main Dashboard
- View current oil price and key metrics
- Explore historical price trends
- Toggle moving averages and Bollinger Bands
- Analyze volatility patterns

### 2. Event Analysis
- See how geopolitical events affected prices
- Filter by event type (Economic, Geopolitical, etc.)
- Adjust analysis window (7-90 days)
- Explore event timeline

### 3. Change Point Analysis
- View detected structural breaks
- Compare before/after statistics
- Understand major market shifts

---

## 🔧 Common Issues & Solutions

### Backend Won't Start
**Problem:** Port 5000 already in use
**Solution:** 
```bash
# Find and kill process using port 5000
lsof -ti:5000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :5000   # Windows
```

### Frontend Won't Start
**Problem:** Port 3000 already in use
**Solution:** Edit `frontend/vite.config.js` and change port

### Module Not Found
**Problem:** Missing dependencies
**Solution:**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules
npm install
```

### Data Not Loading
**Problem:** CSV files not found
**Solution:** Ensure these files exist:
- `data/raw/BrentOilPrices.csv`
- `references/geopolitical_events.csv`

---

## 📊 Using the Dashboard

### Date Range Filtering
1. Click on date range filter
2. Select custom dates OR choose preset (Last Year, 3 Years, etc.)
3. Click "Apply"
4. All charts update automatically

### Event Filtering
1. Go to Event Analysis page
2. Select event type from dropdown
3. Adjust analysis window
4. View updated correlation chart

### Chart Interactions
- **Hover** over data points for details
- **Toggle** indicators (MA, Bollinger Bands)
- **Click** events in timeline to expand
- **Zoom** by scrolling on charts

---

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Main dashboard UI |
| Backend API | http://localhost:5000 | REST API |
| Health Check | http://localhost:5000/api/health | API status |
| Data Summary | http://localhost:5000/api/data/summary | Quick stats |

---

## 📱 Mobile Access

The dashboard is fully responsive! Access from:
- 📱 Smartphones
- 📱 Tablets
- 💻 Laptops
- 🖥️ Desktops

---

## 🛑 Stopping the Dashboard

### Automated Scripts
Press `Ctrl+C` in the terminal

### Manual Stop
Close both terminal windows or press `Ctrl+C` in each

---

## 📚 Need More Help?

- **Setup Issues:** See [`DASHBOARD_README.md`](DASHBOARD_README.md:1)
- **API Details:** See [`API_DOCUMENTATION.md`](API_DOCUMENTATION.md:1)
- **Full Features:** See [`DASHBOARD_DELIVERABLES.md`](DASHBOARD_DELIVERABLES.md:1)

---

## 🎉 You're Ready!

Open http://localhost:3000 and start exploring Brent oil price analysis!

**Pro Tips:**
- 💡 Start with the Main Dashboard for an overview
- 💡 Use Event Analysis to understand price drivers
- 💡 Check Change Points for major market shifts
- 💡 Experiment with date ranges and filters

---

**Happy Analyzing! 📈**
