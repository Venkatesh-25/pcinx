# 🚀 FRA Atlas DSS - Quick Start Guide

## Smart India Hackathon 2025 - Complete System Deployment

### **📋 Prerequisites**

#### **For Frontend Only (Current Working)**
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Local HTTP server (optional but recommended)

#### **For Full Backend (Production)**
- Docker & Docker Compose
- OR Python 3.8+ with pip
- PostgreSQL 12+ with PostGIS extension

---

## **🎯 Option 1: Frontend Demo (Immediate - No Setup)**

### **Quick Demo Access**
```bash
# Open directly in browser
open index.html
# OR
open index-modular.html
```

### **With HTTP Server (Recommended)**
```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx serve .

# Using PHP
php -S localhost:8000

# Then visit: http://localhost:8000
```

### **✅ What You'll See**
- **Interactive Map** with 4 states (Odisha, MP, Tripura, Telangana)
- **10 FRA Claims** with detailed information
- **NDVI Monitoring** with before/after analysis
- **Alert System** with deforestation indicators
- **Dashboard Statistics** with live metrics
- **Report Generation** with downloadable data

---

## **🎯 Option 2: Full Backend Development**

### **Quick Setup with Docker**
```bash
# Navigate to deployment directory
cd deployment/

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend

# Access points:
# Frontend: http://localhost
# Backend API: http://localhost/api
# Database: localhost:5432
```

### **Manual Setup (Development)**
```bash
# 1. Setup Backend
cd backend/
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure Environment
cp .env.example .env
# Edit .env with your database credentials

# 3. Setup Database (PostgreSQL + PostGIS)
createdb fra_atlas_db
psql -d fra_atlas_db -c "CREATE EXTENSION postgis;"

# 4. Initialize Application
python init_db.py
python init_db.py load-data

# 5. Run Development Server
python run.py
```

---

## **🌍 System Architecture Overview**

### **Current Frontend (Working)**
```
Browser → Static Files → GeoJSON Data → Leaflet Map
```

### **Full System (Production Ready)**
```
Browser → Nginx → Flask API → PostgreSQL/PostGIS
                ↓
            Redis Cache
                ↓
         Celery Workers
```

---

## **📊 Data & Features Available**

### **Geographic Coverage**
- **Odisha**: 3 claims (coastal/mangrove areas)
- **Madhya Pradesh**: 2 claims (central forests)
- **Tripura**: 2 claims (northeast hills)
- **Telangana**: 3 claims (Deccan plateau)

### **Monitoring Capabilities**
- **NDVI Analysis**: Vegetation health monitoring
- **Change Detection**: Before/after comparison
- **Alert System**: Automated deforestation alerts
- **Time Series**: Historical trend analysis

### **Dashboard Features**
- **Claim Statistics**: Approval rates, processing times
- **Community Impact**: Families protected, area secured
- **Environmental Metrics**: NDVI trends, alert counts
- **Export Options**: JSON, CSV, PDF reports

---

## **🔌 API Integration (Backend)**

### **Sample API Calls**
```javascript
// Get all claims
fetch('/api/claims/statistics')
  .then(response => response.json())
  .then(data => console.log(data));

// Get NDVI analysis
fetch('/api/monitoring/ndvi/CFR-2024-OD-001')
  .then(response => response.json())
  .then(data => console.log(data));

// Get dashboard stats
fetch('/api/analytics/dashboard')
  .then(response => response.json())
  .then(data => updateDashboard(data));
```

### **API Documentation**
```bash
# API Documentation available at:
http://localhost:5000/          # API overview
http://localhost:5000/health    # Health check
```

---

## **🎨 Frontend Customization**

### **Switching Between Versions**
- **`index.html`** - All-in-one monolithic version
- **`index-modular.html`** - Modular component version
- **`analytics.html`** - Analytics-focused dashboard

### **Configuration Options**
```javascript
// In js/app.js
const CONFIG = {
    API_BASE: 'http://localhost:5000/api',  // Backend API
    NDVI_THRESHOLD: 0.3,                    // Alert threshold
    AUTO_REFRESH: 30000,                    // Refresh interval
    ENABLE_ALERTS: true                     // Sound alerts
};
```

---

## **📈 Performance & Monitoring**

### **System Health Checks**
```bash
# Backend health
curl http://localhost:5000/health

# Database connection
curl http://localhost:5000/api/claims/statistics

# Frontend performance
lighthouse http://localhost/
```

### **Log Monitoring**
```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f postgres

# Application logs
tail -f backend/logs/fra_atlas.log
```

---

## **🔧 Troubleshooting**

### **Common Issues**

#### **Frontend Not Loading**
- Check browser console for errors
- Verify HTTP server is running
- Ensure GeoJSON files are accessible

#### **Backend Connection Issues**
- Verify Docker containers are running
- Check database connection in .env
- Ensure PostgreSQL has PostGIS extension

#### **Performance Issues**
- Enable Redis caching
- Check database indexes
- Monitor container resources

### **Quick Fixes**
```bash
# Restart services
docker-compose restart

# Rebuild containers
docker-compose up --build

# Clear cache
docker-compose exec redis redis-cli FLUSHALL

# Reset database
docker-compose exec postgres psql -U fra_user -d fra_atlas_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

---

## **🎯 SIH 2025 Presentation Setup**

### **Recommended Demo Flow**
1. **Start with Frontend Demo** (immediate impact)
2. **Show Interactive Features** (map, claims, NDVI)
3. **Demonstrate Analytics** (dashboard, reports)
4. **Highlight Technical Architecture** (backend APIs)
5. **Showcase Scalability** (Docker deployment)

### **Key Talking Points**
- ✅ **Real multi-state data** (4 states, 10 claims)
- ✅ **Satellite monitoring** (NDVI analysis)
- ✅ **Production-ready** (Docker, APIs, database)
- ✅ **Scalable architecture** (microservices)
- ✅ **Community impact** (families, hectares protected)

---

## **📞 Support & Next Steps**

### **Immediate Use**
Your system is **ready for demonstration** with the frontend providing full functionality using static data.

### **Production Deployment**
The backend provides enterprise-level capabilities for real-world deployment with live satellite data integration.

### **Future Enhancements**
- Mobile application development
- Real-time satellite data feeds
- Machine learning prediction models
- Multi-language support
- Advanced user authentication

---

**🎉 Your FRA Atlas DSS is complete and ready for Smart India Hackathon 2025!**