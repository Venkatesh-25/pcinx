/**
 * Map Manager - Handles all map-related functionality
 * Manages Leaflet map, overlays, and data loading
 */

class MapManager {
    constructor(mapElementId) {
        this.mapElementId = mapElementId;
        this.map = null;
        this.claimsGroup = null;
        this.beforeOverlay = null;
        this.afterOverlay = null;
        this.fallbackClaim = null;
        
        this.initializeMap();
        this.createNDVIOverlays();
        this.setupFallbackData();
    }

    /**
     * Initialize the Leaflet map
     */
    initializeMap() {
        // Initialize the map centered on India
        this.map = L.map(this.mapElementId, {
            center: [20.2961, 85.8245],
            zoom: 12,
            zoomControl: false
        });

        // Add zoom control to top right
        L.control.zoom({
            position: 'topright'
        }).addTo(this.map);

        // Base layers
        const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
            maxZoom: 18,
        }).addTo(this.map);

        const positron = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://carto.com/attributions">CARTO</a>, &copy; OpenStreetMap contributors',
            maxZoom: 19
        });

        // Initialize claims group
        this.claimsGroup = L.layerGroup().addTo(this.map);

        // Layer Controls
        const baseMaps = { 
            "OpenStreetMap": osm, 
            "Positron (Light)": positron 
        };
        const overlayMaps = { 
            "FRA Claims": this.claimsGroup 
        };
        
        L.control.layers(baseMaps, overlayMaps, { 
            position: 'topright', 
            collapsed: true 
        }).addTo(this.map);

        // Add scale control
        L.control.scale({
            position: 'bottomright'
        }).addTo(this.map);
    }

    /**
     * Create NDVI overlay visualizations
     */
    createNDVIOverlays() {
        const imageBounds = [[20.2900, 85.8100], [20.3100, 85.8300]];
        
        const beforeImageData = this.createNDVIVisualization('before');
        const afterImageData = this.createNDVIVisualization('after');

        this.beforeOverlay = L.imageOverlay(beforeImageData, imageBounds, {
            opacity: 0.6,
            interactive: false
        });

        this.afterOverlay = L.imageOverlay(afterImageData, imageBounds, {
            opacity: 0.6,
            interactive: false
        });
    }

    /**
     * Create NDVI visualization using Canvas
     */
    createNDVIVisualization(type) {
        const canvas = document.createElement('canvas');
        canvas.width = 200;
        canvas.height = 200;
        const ctx = canvas.getContext('2d');
        
        if (type === 'before') {
            // Create gradient for healthy vegetation (green)
            const gradient = ctx.createLinearGradient(0, 0, 200, 200);
            gradient.addColorStop(0, 'rgba(76, 175, 80, 0.7)');
            gradient.addColorStop(1, 'rgba(139, 195, 74, 0.7)');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, 0, 200, 200);
        } else {
            // Create pattern for deforestation (red patches)
            ctx.fillStyle = 'rgba(76, 175, 80, 0.7)'; // Base green
            ctx.fillRect(0, 0, 200, 200);
            
            // Add red patches for deforestation
            ctx.fillStyle = 'rgba(244, 67, 54, 0.8)';
            ctx.fillRect(60, 80, 80, 40);  // Main deforested area
            ctx.fillRect(120, 140, 40, 30); // Secondary patch
            ctx.fillRect(30, 150, 50, 25);  // Third patch
        }
        
        return canvas.toDataURL();
    }

    /**
     * Setup fallback claim data
     */
    setupFallbackData() {
        this.fallbackClaim = {
            "type": "Feature",
            "properties": {
                "name": "CFR-2024-OD-101",
                "village": "Khandagiri",
                "district": "Khurda",
                "area": "245 hectares",
                "status": "Approved",
                "claimants": "127 families",
                "approval_date": "2024-03-15"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [85.8100, 20.3100],
                    [85.8300, 20.3100],
                    [85.8300, 20.2900],
                    [85.8100, 20.2900],
                    [85.8100, 20.3100]
                ]]
            }
        };
    }

    /**
     * Load multi-state data files
     */
    async loadStateData(stateFiles) {
        const loadedFeatures = [];
        let successCount = 0;
        
        for (const file of stateFiles) {
            try {
                const resp = await fetch(file, { cache: 'no-store' });
                if (!resp.ok) throw new Error('HTTP ' + resp.status);
                const data = await resp.json();
                loadedFeatures.push(...data.features);
                successCount++;
                console.log(`✅ Loaded ${file} - ${data.features.length} claims`);
            } catch (err) {
                console.warn(`⚠️ Could not load ${file}:`, err.message);
            }
        }
        
        if (loadedFeatures.length > 0) {
            this.displayLoadedData(loadedFeatures, successCount, stateFiles.length);
        } else {
            this.displayFallbackData();
        }
        
        return loadedFeatures;
    }

    /**
     * Display loaded GeoJSON data on map
     */
    displayLoadedData(features, successCount, totalFiles) {
        this.claimsGroup.clearLayers();
        const allStatesData = { type: 'FeatureCollection', features: features };
        
        const loaded = L.geoJSON(allStatesData, {
            style: (feature) => this.getFeatureStyle(feature),
            onEachFeature: (feature, layer) => this.bindFeaturePopup(feature, layer)
        });
        
        this.claimsGroup.addLayer(loaded);
        
        // Fit map to show all loaded claims
        try { 
            this.map.fitBounds(loaded.getBounds(), { padding: [50,50] }); 
        } catch (e) {
            // Fallback to India center if bounds calculation fails
            this.map.setView([20.5937, 78.9629], 6);
        }
        
        console.log(`🌳 Successfully loaded ${successCount}/${totalFiles} state datasets with ${features.length} total claims`);
        
        // Show initial popup after delay
        setTimeout(() => this.showInitialPopup(), 2500);
    }

    /**
     * Display fallback data when external files can't be loaded
     */
    displayFallbackData() {
        console.warn('Could not load any external GeoJSON files, using built-in sample. Tip: run a local server for full demo.');
        
        const claimLayer = L.geoJSON(this.fallbackClaim, {
            style: {
                color: "#ff7800",
                weight: 3,
                opacity: 0.8,
                fillOpacity: 0.2,
                fillColor: "#ff7800"
            },
            onEachFeature: (feature, layer) => this.bindFallbackPopup(feature, layer)
        });
        
        this.claimsGroup.addLayer(claimLayer);
        try { 
            this.map.fitBounds(claimLayer.getBounds(), { padding: [20,20] }); 
        } catch (e) {}
    }

    /**
     * Get styling for map features based on properties
     */
    getFeatureStyle(feature) {
        const status = (feature.properties.status || '').toLowerCase();
        const hasAlert = feature.properties.deforestation_detected;
        
        let color = '#ff7800'; // default orange
        if (status.includes('pending')) color = '#f1c40f';      // yellow
        else if (status.includes('reject')) color = '#c0392b';  // red
        else if (status.includes('review')) color = '#8e44ad';  // purple
        else if (status.includes('approved')) color = '#27ae60'; // green
        
        return { 
            color: hasAlert ? '#e74c3c' : color, 
            weight: hasAlert ? 3.5 : 2.5, 
            fillColor: color, 
            fillOpacity: hasAlert ? 0.4 : 0.2,
            dashArray: hasAlert ? '5, 5' : null
        };
    }

    /**
     * Bind popup to feature
     */
    bindFeaturePopup(feature, layer) {
        const props = feature.properties;
        const status = props.status || 'Unknown';
        const name = props.claim_id || props.name || 'Claim';
        const area = props.area_hectares ? props.area_hectares + ' ha' : (props.area || '—');
        const village = props.village_name || props.village || '—';
        const district = props.district || '—';
        const state = props.state || '—';
        const families = props.claimant_families || '—';
        
        const alert = props.deforestation_detected ? 
            '<div style="color:#e74c3c;font-weight:600;background:#fff5f5;padding:5px;border-radius:4px;margin-top:8px;">🚨 DEFORESTATION ALERT</div>' : 
            '<div style="color:#27ae60;font-weight:600;">✅ No Active Alerts</div>';
        
        const popupContent = `
            <div style="min-width:250px; font-family: inherit;">
                <h4 style="margin:0 0 10px;color:#2d5016;border-bottom:2px solid #e1e1e1;padding-bottom:5px">${name}</h4>
                <p><strong>State:</strong> ${state}</p>
                <p><strong>Village:</strong> ${village}</p>
                <p><strong>District:</strong> ${district}</p>
                <p><strong>Status:</strong> <span style="color:${this.getStatusColor(status)};font-weight:600">${status}</span></p>
                <p><strong>Area:</strong> ${area}</p>
                <p><strong>Families:</strong> ${families}</p>
                ${alert}
            </div>
        `;
        
        layer.bindPopup(popupContent, {
            maxWidth: 300,
            className: 'custom-popup'
        });
    }

    /**
     * Bind popup to fallback feature
     */
    bindFallbackPopup(feature, layer) {
        const props = feature.properties;
        const popupContent = `
            <div style="font-family: inherit; min-width: 200px;">
                <h4 style="margin: 0 0 10px 0; color: #2d5016;">
                    <i class="fas fa-map-marker-alt"></i> ${props.name}
                </h4>
                <p><strong>Village:</strong> ${props.village}</p>
                <p><strong>District:</strong> ${props.district}</p>
                <p><strong>Area:</strong> ${props.area}</p>
                <p><strong>Status:</strong> <span style="color: green; font-weight: bold;">${props.status}</span></p>
                <p><strong>Beneficiaries:</strong> ${props.claimants}</p>
                <p><strong>Approved:</strong> ${props.approval_date}</p>
            </div>
        `;
        
        layer.bindPopup(popupContent, {
            className: 'popup-custom'
        });
    }

    /**
     * Get color for claim status
     */
    getStatusColor(status) {
        const s = status.toLowerCase();
        if (s.includes('approved')) return '#27ae60';
        if (s.includes('pending')) return '#f39c12';
        if (s.includes('review')) return '#8e44ad';
        if (s.includes('reject')) return '#c0392b';
        return '#34495e';
    }

    /**
     * Show initial guidance popup
     */
    showInitialPopup() {
        try {
            const layers = this.claimsGroup.getLayers();
            if (layers.length > 0) {
                const firstLayer = layers[0];
                const innerLayers = firstLayer.getLayers ? firstLayer.getLayers() : [firstLayer];
                if (innerLayers.length > 0 && innerLayers[0].openPopup) {
                    innerLayers[0].openPopup();
                }
            }
        } catch (e) {
            console.warn('Could not open initial popup:', e);
        }
    }

    /**
     * Show before NDVI overlay
     */
    showBeforeOverlay() {
        this.showLoading();
        setTimeout(() => {
            this.map.removeLayer(this.afterOverlay);
            this.beforeOverlay.addTo(this.map);
            this.hideLoading();
            
            // Show info popup
            const popup = L.popup()
                .setLatLng([20.3000, 85.8200])
                .setContent('<div style="text-align: center;"><strong>January 2025</strong><br>Healthy Forest Cover<br>NDVI: 0.75 (High)</div>')
                .openOn(this.map);
                
            setTimeout(() => this.map.closePopup(), 3000);
        }, 1500);
    }

    /**
     * Show after NDVI overlay
     */
    showAfterOverlay() {
        this.showLoading();
        setTimeout(() => {
            this.map.removeLayer(this.beforeOverlay);
            this.afterOverlay.addTo(this.map);
            this.hideLoading();
            
            // Show alert popup
            const popup = L.popup()
                .setLatLng([20.2980, 85.8150])
                .setContent('<div style="text-align: center; color: #d32f2f;"><strong>⚠️ September 2025</strong><br>Deforestation Detected<br>NDVI: 0.21 (Critical)</div>')
                .openOn(this.map);
                
            setTimeout(() => this.map.closePopup(), 4000);
        }, 1500);
    }

    /**
     * Reset map view
     */
    resetView() {
        this.map.removeLayer(this.beforeOverlay);
        this.map.removeLayer(this.afterOverlay);
        this.map.setView([20.2961, 85.8245], 12);
    }

    /**
     * Show loading indicator
     */
    showLoading() {
        const loading = document.getElementById('loading');
        if (loading) loading.style.display = 'block';
    }

    /**
     * Hide loading indicator
     */
    hideLoading() {
        const loading = document.getElementById('loading');
        if (loading) loading.style.display = 'none';
    }

    /**
     * Get the map instance
     */
    getMap() {
        return this.map;
    }
}