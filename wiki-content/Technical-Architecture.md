# Technical Architecture

## 🏗️ System Design & Architecture Overview

The FRA Atlas MVP is architected with **simplicity, scalability, and maintainability** as core principles. Our modular design enables rapid development while maintaining enterprise-grade code organization.

### 🎯 Architecture Philosophy

#### **Zero-Dependency Frontend**
- **Pure Web Technologies**: HTML5, CSS3, Vanilla JavaScript
- **No Build Process**: Direct browser execution without compilation
- **Minimal External Dependencies**: Only Leaflet.js and Font Awesome via CDN
- **Progressive Enhancement**: Works without JavaScript for basic content

#### **Component-Based Design**
- **Separation of Concerns**: Each module handles specific functionality
- **Loose Coupling**: Components communicate through well-defined interfaces
- **High Cohesion**: Related functionality grouped together
- **Testable Architecture**: Easy unit testing and integration testing

### 🗂️ Project Structure Deep Dive

```
fra-atlas-mvp/
├── 📄 index.html                    # Production-ready single file
├── 📄 index-modular.html            # Development-friendly modular version
├── 🎨 css/                          # Modular stylesheets
│   ├── main.css                     # Core layout, animations, loading states
│   ├── dashboard.css                # Statistics, controls, alerts
│   ├── modal.css                    # Forms, dialogs, overlays
│   └── map.css                      # Leaflet styling, legends, popups
├── ⚡ js/                           # JavaScript modules
│   ├── app.js                       # Main application coordinator
│   └── components/                  # Reusable component modules
│       ├── map-manager.js           # Leaflet map operations
│       ├── dashboard.js             # Statistics and analytics
│       └── report-modal.js          # Issue reporting system
├── 🗃️ data/                        # Spatial data files
│   ├── odisha_fra.geojson          # State boundary data
│   ├── mp_fra.geojson              # Sample FRA claims
│   ├── tripura_fra.geojson         # Geospatial polygons
│   └── telangana_fra.geojson       # Administrative boundaries
└── 📚 docs/                        # Documentation and assets
```

### 🧩 Component Architecture

#### **1. Main Application (`js/app.js`)**

```javascript
class FRAAtlasApp {
    constructor() {
        this.mapManager = null;
        this.dashboard = null;
        this.reportModal = null;
    }
    
    async init() {
        // Initialize all components
        // Set up event listeners
        // Load initial data
    }
}
```

**Responsibilities:**
- Application lifecycle management
- Component initialization and coordination
- Global event handling and state management
- Error handling and logging

#### **2. Map Manager (`js/components/map-manager.js`)**

```javascript
class MapManager {
    constructor(containerId) {
        this.map = null;
        this.currentOverlay = null;
        this.fraLayers = new Map();
    }
    
    initializeMap() {
        // Leaflet map setup
        // Base layer configuration
        // Control initialization
    }
    
    loadStateData(stateCode) {
        // GeoJSON data loading
        // Layer management
        // Popup configuration
    }
    
    toggleNDVIOverlay(type) {
        // NDVI visualization
        // Before/after comparison
        // Color mapping
    }
}
```

**Responsibilities:**
- Leaflet.js map initialization and management
- GeoJSON data loading and visualization
- NDVI overlay generation and display
- Interactive popup and tooltip handling
- Layer management and switching

#### **3. Dashboard (`js/components/dashboard.js`)**

```javascript
class Dashboard {
    constructor() {
        this.currentStats = {};
        this.updateInterval = null;
    }
    
    updateStatistics(newStats) {
        // Animated counter updates
        // Chart regeneration
        // Alert management
    }
    
    startRealTimeUpdates() {
        // Simulated live data
        // Periodic updates
        // Change detection
    }
}
```

**Responsibilities:**
- Statistics display and real-time updates
- Alert system management
- Performance metrics calculation
- Data visualization and charting

#### **4. Report Modal (`js/components/report-modal.js`)**

```javascript
class ReportModal {
    constructor() {
        this.modal = null;
        this.form = null;
        this.isOpen = false;
    }
    
    show() {
        // Modal display logic
        // Form initialization
        // Validation setup
    }
    
    submitReport(formData) {
        // Form validation
        // Data processing
        // Submission handling
    }
}
```

**Responsibilities:**
- Modal dialog management
- Form validation and submission
- Issue categorization and processing
- GPS coordinate handling

### 🎨 CSS Architecture

#### **Modular Stylesheet Organization**

##### **1. Core Styles (`css/main.css`)**
```css
/* Global variables and resets */
:root {
    --primary-color: #2d5016;
    --secondary-color: #4CAF50;
    --accent-color: #8BC34A;
    /* ... */
}

/* Layout foundations */
.main-container { /* Grid layout */ }
.header { /* Navigation and branding */ }
.loading { /* Loading states and animations */ }
```

##### **2. Dashboard Styles (`css/dashboard.css`)**
```css
/* Statistics and controls */
.dashboard { /* Sidebar layout */ }
.stat-card { /* Metric display cards */ }
.control-btn { /* Interactive buttons */ }
.alert { /* Notification system */ }
```

##### **3. Modal Styles (`css/modal.css`)**
```css
/* Forms and dialogs */
.modal { /* Overlay and positioning */ }
.modal-content { /* Dialog styling */ }
.form-group { /* Input field layouts */ }
.submit-btn { /* Action buttons */ }
```

##### **4. Map Styles (`css/map.css`)**
```css
/* Leaflet customizations */
#map { /* Map container */ }
.legend { /* Map legend styling */ }
.leaflet-popup { /* Popup customizations */ }
.leaflet-control { /* Control styling */ }
```

### 🗃️ Data Architecture

#### **GeoJSON Structure**

```json
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[lat, lng], ...]]
            },
            "properties": {
                "claim_id": "OD_2023_001",
                "village": "Kendrapada Village",
                "district": "Kendrapada",
                "state": "Odisha",
                "status": "approved",
                "area_hectares": 15.67,
                "families_count": 23,
                "claim_date": "2023-03-15",
                "approval_date": "2023-08-20"
            }
        }
    ]
}
```

#### **NDVI Data Simulation**

```javascript
// Simulated NDVI calculation
function generateNDVI(lat, lng, timestamp) {
    const baseline = 0.7; // Healthy vegetation
    const degradation = calculateDegradation(lat, lng, timestamp);
    return Math.max(0, baseline - degradation);
}

// Color mapping for visualization
const ndviColorScale = {
    high: '#2d5016',    // Healthy forest (NDVI > 0.6)
    medium: '#8BC34A',  // Moderate vegetation (0.3-0.6)
    low: '#ff6b6b',     // Degraded/deforested (< 0.3)
    water: '#2196F3'    // Water bodies
};
```

### 🔄 Data Flow Architecture

#### **Application Initialization Flow**

```mermaid
graph TD
    A[Browser Load] --> B[DOM Ready]
    B --> C[FRAAtlasApp.init()]
    C --> D[Initialize MapManager]
    C --> E[Initialize Dashboard]
    C --> F[Initialize ReportModal]
    D --> G[Load Map Tiles]
    D --> H[Load GeoJSON Data]
    E --> I[Start Statistics Updates]
    H --> J[Display FRA Boundaries]
    I --> K[Update Dashboard UI]
    J --> L[Application Ready]
    K --> L
```

#### **User Interaction Flow**

```mermaid
graph TD
    A[User Action] --> B{Action Type}
    B -->|Map Click| C[MapManager.handleClick()]
    B -->|NDVI Toggle| D[MapManager.toggleNDVIOverlay()]
    B -->|Report Issue| E[ReportModal.show()]
    B -->|Dashboard Update| F[Dashboard.updateStatistics()]
    C --> G[Display Popup]
    D --> H[Generate NDVI Layer]
    E --> I[Show Modal Form]
    F --> J[Animate Counters]
```

### 🔧 API Design Patterns

#### **Component Communication**

```javascript
// Event-driven architecture
class ComponentBase {
    constructor() {
        this.eventListeners = new Map();
    }
    
    emit(eventName, data) {
        const listeners = this.eventListeners.get(eventName) || [];
        listeners.forEach(callback => callback(data));
    }
    
    on(eventName, callback) {
        const listeners = this.eventListeners.get(eventName) || [];
        listeners.push(callback);
        this.eventListeners.set(eventName, listeners);
    }
}

// Usage example
mapManager.on('claimSelected', (claimData) => {
    dashboard.highlightClaim(claimData.claim_id);
    analytics.trackClaimView(claimData);
});
```

#### **State Management Pattern**

```javascript
class StateManager {
    constructor() {
        this.state = {
            selectedState: null,
            selectedClaim: null,
            currentNDVILayer: null,
            dashboardStats: {},
            alerts: []
        };
        this.subscribers = new Set();
    }
    
    setState(updates) {
        this.state = { ...this.state, ...updates };
        this.notifySubscribers();
    }
    
    subscribe(callback) {
        this.subscribers.add(callback);
        return () => this.subscribers.delete(callback);
    }
}
```

### 🚀 Performance Optimization

#### **Loading Strategy**

```javascript
// Progressive loading
async function loadApplicationData() {
    // 1. Load critical UI first
    await loadCriticalCSS();
    
    // 2. Initialize map with basic tiles
    await initializeBasicMap();
    
    // 3. Load GeoJSON data progressively
    const states = ['odisha', 'mp', 'tripura', 'telangana'];
    for (const state of states) {
        loadStateDataAsync(state); // Non-blocking
    }
    
    // 4. Start real-time updates
    startDashboardUpdates();
}
```

#### **Memory Management**

```javascript
class MapManager {
    clearLayers() {
        // Clean up Leaflet layers
        this.fraLayers.forEach(layer => {
            this.map.removeLayer(layer);
            layer.clearAllEventListeners();
        });
        this.fraLayers.clear();
    }
    
    optimizePerformance() {
        // Throttle map events
        const throttledUpdate = throttle(this.updateView.bind(this), 100);
        this.map.on('moveend', throttledUpdate);
        
        // Debounce search inputs
        const debouncedSearch = debounce(this.searchLocations.bind(this), 300);
        searchInput.addEventListener('input', debouncedSearch);
    }
}
```

### 🔐 Security Considerations

#### **Input Validation**

```javascript
class ReportModal {
    validateInput(formData) {
        const validators = {
            issueType: (value) => ['deforestation', 'encroachment', 'mining', 'dumping', 'other'].includes(value),
            reporterName: (value) => /^[a-zA-Z\s]{2,50}$/.test(value),
            coordinates: (value) => !value || /^-?\d+\.?\d*,-?\d+\.?\d*$/.test(value),
            description: (value) => value.length >= 10 && value.length <= 1000
        };
        
        const errors = {};
        Object.keys(validators).forEach(field => {
            if (!validators[field](formData[field])) {
                errors[field] = `Invalid ${field}`;
            }
        });
        
        return { isValid: Object.keys(errors).length === 0, errors };
    }
}
```

#### **XSS Prevention**

```javascript
function sanitizeHTML(input) {
    const div = document.createElement('div');
    div.textContent = input;
    return div.innerHTML;
}

function safeInsertHTML(element, content) {
    element.textContent = ''; // Clear first
    element.insertAdjacentHTML('afterbegin', DOMPurify.sanitize(content));
}
```

### 📱 Responsive Design Architecture

#### **Mobile-First Approach**

```css
/* Mobile-first responsive design */
.dashboard {
    /* Mobile layout by default */
    width: 100%;
    position: fixed;
    bottom: 0;
    height: 40vh;
}

/* Tablet and up */
@media (min-width: 768px) {
    .dashboard {
        position: relative;
        width: 350px;
        height: 100vh;
    }
}

/* Desktop optimization */
@media (min-width: 1200px) {
    .dashboard {
        width: 400px;
    }
    
    .stat-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}
```

### 🔮 Scalability Considerations

#### **Future Extension Points**

1. **Backend API Integration**
   - Replace static GeoJSON with REST API calls
   - Add authentication and user management
   - Implement real-time WebSocket connections

2. **Database Integration**
   - PostgreSQL with PostGIS for spatial data
   - Time-series database for satellite imagery
   - Caching layer with Redis

3. **Microservices Architecture**
   - Separate services for map data, analytics, notifications
   - API Gateway for request routing
   - Container orchestration with Docker/Kubernetes

4. **Advanced Analytics**
   - Machine learning integration for predictive analysis
   - Real-time satellite data processing
   - Advanced visualization with D3.js or Three.js

### 📊 Testing Architecture

#### **Component Testing Strategy**

```javascript
// Example test structure
describe('MapManager', () => {
    let mapManager;
    
    beforeEach(() => {
        // Set up test environment
        document.body.innerHTML = '<div id="test-map"></div>';
        mapManager = new MapManager('test-map');
    });
    
    test('should initialize map correctly', () => {
        mapManager.initializeMap();
        expect(mapManager.map).toBeDefined();
        expect(mapManager.map.getZoom()).toBe(6);
    });
    
    test('should load GeoJSON data', async () => {
        const mockData = { type: 'FeatureCollection', features: [] };
        global.fetch = jest.fn().mockResolvedValue({
            json: () => Promise.resolve(mockData)
        });
        
        await mapManager.loadStateData('odisha');
        expect(mapManager.fraLayers.size).toBe(1);
    });
});
```

---

**This modular architecture ensures the FRA Atlas MVP is maintainable, scalable, and ready for enterprise-level enhancements while maintaining simplicity for rapid development and deployment.** 🏗️