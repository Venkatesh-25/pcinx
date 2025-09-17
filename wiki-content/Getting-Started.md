# Getting Started with FRA Atlas MVP

## 🚀 Quick Start Guide

This guide will help you get the FRA Atlas MVP running locally on your machine in just a few minutes.

### 📋 Prerequisites

#### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux Ubuntu 18.04+
- **Web Browser**: Chrome 80+, Firefox 75+, Edge 80+, Safari 13+
- **Internet Connection**: Required for map tiles and external resources
- **Git**: For cloning the repository (optional if downloading ZIP)

#### No Installation Required ✨
The FRA Atlas MVP is built with **zero dependencies** and runs directly in your browser without any build process or server setup!

### 🔄 Installation Methods

#### Method 1: Direct Browser Access (Recommended for Demo)
1. **Visit Live Demo**: [https://ultrabot05.github.io/fra-atlas-mvp/](https://ultrabot05.github.io/fra-atlas-mvp/)
2. **Instant Access**: No installation required, works immediately
3. **Full Functionality**: All features available online

#### Method 2: Local Setup (Recommended for Development)

##### Option A: Git Clone
```bash
# Clone the repository
git clone https://github.com/UltraBot05/fra-atlas-mvp.git

# Navigate to project directory
cd fra-atlas-mvp

# Open in browser
# Windows
start index.html
# macOS
open index.html
# Linux
xdg-open index.html
```

##### Option B: Download ZIP
1. Visit [GitHub Repository](https://github.com/UltraBot05/fra-atlas-mvp)
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Open `index.html` in your web browser

#### Method 3: Local Web Server (Optional for Development)

If you prefer running with a local server (useful for development):

```bash
# Python 3.x
python -m http.server 8000
# Then open: http://localhost:8000

# Python 2.x
python -m SimpleHTTPServer 8000

# Node.js (if you have it installed)
npx http-server
# or
npm install -g http-server
http-server

# PHP (if installed)
php -S localhost:8000
```

### 🏗️ Project Structure

```
fra-atlas-mvp/
├── index.html              # Main application (original single file)
├── index-modular.html      # Modular architecture version
├── README.md               # Project documentation
├── SIH_2025_COMPLETION_SUMMARY.md
├── css/                    # Modular stylesheets
│   ├── main.css           # Core layout and animations
│   ├── dashboard.css      # Statistics and controls
│   ├── modal.css          # Forms and dialogs
│   └── map.css            # Map styling and legend
├── js/                     # JavaScript modules
│   ├── app.js             # Main application coordinator
│   └── components/        # Component modules
│       ├── map-manager.js     # Map functionality
│       ├── dashboard.js       # Dashboard management
│       └── report-modal.js    # Issue reporting
└── data/                   # Sample GeoJSON data
    ├── odisha_fra.geojson     # Odisha FRA boundaries
    ├── mp_fra.geojson         # Madhya Pradesh data
    ├── tripura_fra.geojson    # Tripura boundaries
    └── telangana_fra.geojson  # Telangana data
```

### 🎮 First Time Usage

#### 1. Open the Application
- **Single File Version**: Open `index.html` for the complete working demo
- **Modular Version**: Open `index-modular.html` for the organized architecture

#### 2. Explore Key Features

##### 🗺️ **Interactive Map**
- **Pan & Zoom**: Use mouse to navigate the map
- **State Selection**: Click on different states to see FRA claim boundaries
- **Popup Information**: Click on claim boundaries for detailed information

##### 🛰️ **Satellite Monitoring**
- **Baseline View**: Click "January 2025 (Baseline)" to see healthy vegetation
- **Current Analysis**: Click "September 2025 (Current)" to see recent changes
- **NDVI Comparison**: Notice the color differences indicating forest health

##### 📊 **Dashboard Analytics**
- **Live Statistics**: View real-time claim counts and status updates
- **Community Impact**: See protected families and secured hectares
- **System Status**: Monitor coverage and last update times

##### 📱 **Issue Reporting**
- **Report Button**: Click "Report Issue" to open the form
- **Form Categories**: Select from deforestation, encroachment, mining, etc.
- **GPS Coordinates**: Optional location precision for reports

### ⚙️ Configuration Options

#### Customizing for Your Region

##### 1. **Adding New GeoJSON Data**
```javascript
// In js/components/map-manager.js, add new data sources
const stateDataSources = {
    'your-state': 'data/your-state_fra.geojson',
    // ... existing states
};
```

##### 2. **Modifying NDVI Thresholds**
```javascript
// In js/components/map-manager.js
const NDVI_THRESHOLD = 0.3; // Adjust deforestation detection sensitivity
```

##### 3. **Customizing Dashboard Metrics**
```javascript
// In js/components/dashboard.js
const initialStats = {
    approved: 234,    // Modify these values
    pending: 156,     // to match your region
    review: 43,
    rejected: 12
};
```

### 🔧 Development Setup

#### For Developers Contributing to the Project

##### 1. **Fork the Repository**
```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/fra-atlas-mvp.git
cd fra-atlas-mvp
```

##### 2. **Set Up Development Environment**
```bash
# Add upstream remote for staying updated
git remote add upstream https://github.com/UltraBot05/fra-atlas-mvp.git

# Create a new feature branch
git checkout -b feature/your-feature-name
```

##### 3. **Development Workflow**
```bash
# Make your changes
# Test in browser

# Commit changes
git add .
git commit -m "feat: your feature description"

# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

### 🐛 Troubleshooting

#### Common Issues and Solutions

##### **Map Not Loading**
- **Check Internet Connection**: Map tiles require internet access
- **Browser Console**: Open DevTools (F12) and check for JavaScript errors
- **CORS Issues**: If running locally, use a local web server instead of file:// protocol

##### **Popup Blockers**
- **Browser Settings**: Ensure popups are allowed for the domain
- **Extensions**: Disable ad blockers temporarily if needed

##### **Performance Issues**
- **Large GeoJSON Files**: Consider simplifying geometries for better performance
- **Browser Memory**: Close other tabs if experiencing slowdowns
- **Hardware Acceleration**: Enable in browser settings for better map rendering

##### **Mobile Display Issues**
- **Viewport Meta Tag**: Ensure `<meta name="viewport" content="width=device-width, initial-scale=1.0">` is present
- **Touch Events**: Use mobile browser for testing touch interactions
- **Screen Size**: Test on various device sizes and orientations

### 📱 Mobile Usage

#### Optimized for Mobile Devices
- **Responsive Design**: Automatically adapts to screen size
- **Touch Controls**: Optimized map interactions for touch devices
- **Mobile Navigation**: Collapsible sidebar for better mobile experience
- **Offline Capabilities**: Basic functionality works with cached resources

#### Mobile Testing
```bash
# Chrome DevTools device simulation
1. Open DevTools (F12)
2. Click device toggle icon
3. Select device type (iPhone, Android, etc.)
4. Test touch interactions and responsive layout
```

### 🌐 Browser Compatibility

| Browser | Version | Status | Notes |
|---------|---------|--------|-------|
| **Chrome** | 80+ | ✅ Full Support | Recommended for development |
| **Firefox** | 75+ | ✅ Full Support | Good performance |
| **Edge** | 80+ | ✅ Full Support | Windows integration |
| **Safari** | 13+ | ✅ Full Support | macOS/iOS optimized |
| **IE 11** | - | ⚠️ Limited | Basic functionality only |

### 🔗 Next Steps

After getting the application running:

1. **Explore Features**: Try all interactive elements and controls
2. **Read Documentation**: Check [User Guide](User-Guide) for detailed feature explanations
3. **Technical Deep Dive**: Review [Technical Architecture](Technical-Architecture) for system design
4. **Contribute**: Follow [Contributing](Contributing) guidelines for development participation
5. **Deploy**: Use [Deployment Guide](Deployment-Guide) for production setup

### 📞 Need Help?

- **Documentation**: Browse other wiki sections for specific topics
- **Issues**: Report problems on [GitHub Issues](https://github.com/UltraBot05/fra-atlas-mvp/issues)
- **Community**: Join discussions and ask questions
- **SIH 2025**: Check [SIH 2025 Documentation](SIH-2025-Documentation) for competition details

---

**Ready to explore forest conservation technology? Let's get started! 🌿**