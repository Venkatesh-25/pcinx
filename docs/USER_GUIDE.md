# 📖 FRA Atlas DSS - User Guide

## Quick Start

### For Judges/Evaluators
1. **Open the Demo**: Double-click `index.html` or visit the GitHub Pages URL
2. **Explore the Map**: Click on orange polygons to see FRA claim details
3. **Test Monitoring**: Use "January 2025" and "September 2025" buttons
4. **View Dashboard**: Check real-time statistics and alerts on the right panel

### For Government Officials
1. **Dashboard Overview**: Monitor claim statistics and system status
2. **Alert Management**: Review deforestation alerts with priority indicators
3. **Report Export**: Generate PDF reports for administrative use
4. **Multi-layer Analysis**: Toggle between base maps and overlay data

### For Tribal Communities
1. **Claim Tracking**: Search and view your community's claim status
2. **Transparency**: Access real-time updates on claim processing
3. **Documentation**: Digital records reduce paperwork requirements

## Key Features

### 🗺️ Interactive Mapping
- **Navigation**: Use mouse to pan and zoom
- **Popups**: Click any claim boundary for detailed information
- **Layers**: Toggle between different map styles and data layers
- **Legend**: Understand color coding and symbols

### 🛰️ Satellite Monitoring
- **Baseline View**: January 2025 shows healthy forest cover
- **Current Analysis**: September 2025 reveals changes and alerts
- **NDVI Scale**: Green = healthy vegetation, Red = deforestation
- **Loading States**: Visual feedback during data processing

### 📊 Dashboard Controls
- **Real-time Stats**: Live updates of claim counts and status
- **Alert System**: Priority-based notifications for urgent issues
- **Export Tools**: Generate reports in PDF format
- **System Status**: Monitor satellite connectivity and data freshness

## Understanding the Data

### Claim Status Types
- **🟢 Approved**: Community Forest Rights granted
- **🟡 Pending**: Application under review
- **🟣 Under Review**: Additional documentation required
- **🔴 Rejected**: Application declined (with reasons)

### Alert Levels
- **🔴 High**: Significant deforestation detected (>50% NDVI drop)
- **🟡 Medium**: Moderate vegetation loss (20-50% NDVI drop)
- **🟢 Low**: Normal seasonal variation (<20% change)

### NDVI Values
- **0.7-1.0**: Dense, healthy vegetation
- **0.3-0.7**: Moderate vegetation cover
- **0.0-0.3**: Sparse vegetation or deforested areas
- **<0.0**: Water bodies or built-up areas

## Troubleshooting

### Map Not Loading
- Check internet connection for base map tiles
- Try refreshing the page
- Ensure JavaScript is enabled in browser

### Missing Claim Data
- If using file:// protocol, some features may be limited
- For full functionality, serve via local HTTP server:
  ```bash
  python -m http.server 8000
  ```

### Performance Issues
- Close other browser tabs to free memory
- Use latest Chrome, Firefox, or Edge browser
- Clear browser cache if experiencing slow loading

## Browser Compatibility
- ✅ **Chrome 80+**: Full functionality
- ✅ **Firefox 75+**: Full functionality  
- ✅ **Edge 80+**: Full functionality
- ⚠️ **Safari 13+**: Limited animation support
- ❌ **IE 11**: Not supported

## Mobile Usage
- **Touch Navigation**: Pinch to zoom, drag to pan
- **Responsive Design**: Optimized for tablets and phones
- **Offline Capability**: Basic functionality without internet
- **Performance**: Optimized for low-bandwidth connections

## Data Sources & Accuracy

### Spatial Data
- **FRA Claims**: Official state portal data (sample for demo)
- **Satellite Imagery**: Sentinel-2 (10m resolution)
- **Administrative Boundaries**: Survey of India datasets
- **Forest Cover**: ISFR 2023 official data

### Update Frequency
- **Claims Data**: Weekly sync with state portals
- **Satellite Monitoring**: Every 5 days (Sentinel-2 revisit)
- **Alerts**: Real-time processing and notification
- **Reports**: Generated on-demand with latest data

## Support Contacts
- **Technical Issues**: [GitHub Issues](link-to-repo)
- **Data Queries**: Team Green Guardians
- **Partnership**: Smart India Hackathon 2025

---
**Problem Statement SIH12508 | Team Green Guardians**
