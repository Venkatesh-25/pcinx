# 🏗️ FRA Atlas DSS - Technical Architecture

## System Overview
The FRA Atlas DSS follows a **client-side first** architecture optimized for rapid prototyping and demonstration, with a clear migration path to full-scale deployment.

## Architecture Layers

### 🎨 Frontend Layer
- **Technology**: HTML5, CSS3, Vanilla JavaScript
- **Mapping**: Leaflet.js (lightweight, no dependencies)
- **Styling**: Custom CSS with glassmorphism design
- **Icons**: Font Awesome 6.0
- **Responsive**: Mobile-first design principles

### 🗺️ Data Layer
- **Format**: GeoJSON for spatial data
- **Storage**: Static files (MVP), Future: PostGIS/MongoDB
- **Sources**: 
  - FRA Atlas datasets (state portals)
  - Sentinel-2 satellite imagery
  - ISFR 2023 forest cover data

### 🛰️ Processing Layer
- **NDVI Calculation**: Client-side canvas rendering (MVP)
- **Future**: Python backend with GDAL/rasterio
- **Satellite Data**: Google Earth Engine API integration planned
- **Alerts**: Rule-based threshold detection

### 📊 Analytics Layer
- **Current**: JavaScript-based statistics
- **Future**: Python analytics pipeline
- **ML Components**: Deforestation prediction models
- **Reporting**: PDF/Excel export capabilities

## MVP vs Production Architecture

### MVP (Current - 2 Days)
```
Browser (Leaflet.js) → Static GeoJSON → Canvas NDVI → Local Storage
```

### POC (2-4 Weeks)
```
Browser → Flask API → SQLite/PostGIS → Sentinel-2 Processing
```

### Production (2-3 Months)
```
React/Mobile App → FastAPI/Django → PostGIS → Microservices → Cloud Storage
```

## Data Flow

### 1. Claim Data Ingestion
- State FRA portals → GeoJSON conversion → Validation → Display

### 2. Satellite Monitoring
- Sentinel-2 Hub → NDVI calculation → Change detection → Alert generation

### 3. Decision Support
- Multi-layer analysis → Dashboard updates → Report generation → Notification system

## Security Considerations
- Client-side processing (no sensitive data transmission)
- HTTPS-ready for production
- Input validation and sanitization
- Role-based access control (planned)

## Scalability Strategy
- **Horizontal**: Multi-state data federation
- **Vertical**: Microservices decomposition
- **Geographic**: CDN for static assets
- **Temporal**: Data archiving and compression

## Technology Migration Path

### Phase 1 (MVP): Static Demo
- ✅ Leaflet + GeoJSON + Canvas
- ✅ Hardcoded NDVI overlays
- ✅ Mock dashboard statistics

### Phase 2 (POC): Dynamic Backend
- [ ] Flask/FastAPI integration
- [ ] Real-time data fetching
- [ ] Basic user authentication

### Phase 3 (Production): Full Stack
- [ ] React frontend with state management
- [ ] Microservices architecture
- [ ] Real-time satellite processing
- [ ] Mobile applications

## Development Setup
```bash
# Current (MVP)
git clone <repo-url>
cd fra-atlas-mvp
python -m http.server 8000  # Optional
open index.html

# Future (Backend)
pip install flask postgis gdal
docker-compose up
```

## API Design (Planned)
```
GET /api/claims?state=odisha&status=pending
GET /api/ndvi/{claim_id}?start_date=2025-01&end_date=2025-09
POST /api/alerts/subscribe
GET /api/reports/export?format=pdf&claim_ids=...
```

---
**Built by Team Green Guardians for SIH 2025**
