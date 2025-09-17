// 🛰️ FRA Atlas DSS - NDVI Calculator
// Client-side NDVI utilities for demonstration and future backend integration

class NDVICalculator {
    constructor() {
        this.HEALTHY_THRESHOLD = 0.6;
        this.ALERT_THRESHOLD = 0.3;
        this.CRITICAL_THRESHOLD = 0.1;
    }

    /**
     * Calculate NDVI from Near-Infrared and Red band values
     * NDVI = (NIR - Red) / (NIR + Red)
     */
    calculateNDVI(nearInfrared, red) {
        if (nearInfrared + red === 0) return 0;
        return (nearInfrared - red) / (nearInfrared + red);
    }

    /**
     * Generate mock NDVI time series for demonstration
     */
    generateMockTimeSeries(startDate, endDate, degradationRate = 0.02) {
        const timeSeries = [];
        const start = new Date(startDate);
        const end = new Date(endDate);
        const daysBetween = Math.ceil((end - start) / (1000 * 60 * 60 * 24));
        
        let baselineNDVI = 0.75; // Healthy forest baseline
        
        for (let i = 0; i <= daysBetween; i += 10) {
            const currentDate = new Date(start.getTime() + (i * 24 * 60 * 60 * 1000));
            const monthsElapsed = i / 30;
            
            // Simulate degradation over time
            let currentNDVI = baselineNDVI - (degradationRate * monthsElapsed);
            
            // Add realistic noise and seasonal variation
            const seasonalFactor = 0.1 * Math.sin((i / 365) * 2 * Math.PI);
            const noise = (Math.random() - 0.5) * 0.1;
            currentNDVI += seasonalFactor + noise;
            
            // Clamp values to realistic range
            currentNDVI = Math.max(0.05, Math.min(0.95, currentNDVI));
            
            timeSeries.push({
                date: currentDate.toISOString().split('T')[0],
                ndvi: Math.round(currentNDVI * 1000) / 1000,
                classification: this.classifyNDVI(currentNDVI),
                confidence: 0.85 + (Math.random() * 0.1) // 85-95% confidence
            });
        }
        
        return timeSeries;
    }

    /**
     * Classify NDVI value into health categories
     */
    classifyNDVI(ndviValue) {
        if (ndviValue >= this.HEALTHY_THRESHOLD) return 'Healthy Vegetation';
        if (ndviValue >= this.ALERT_THRESHOLD) return 'Moderate Vegetation';
        if (ndviValue >= this.CRITICAL_THRESHOLD) return 'Sparse Vegetation';
        return 'Bare Soil/Water';
    }

    /**
     * Detect significant changes in NDVI trend
     */
    detectChanges(timeSeries, alertThreshold = 0.15) {
        const changes = [];
        
        if (timeSeries.length < 2) return changes;
        
        const baseline = timeSeries[0].ndvi;
        
        for (let i = 1; i < timeSeries.length; i++) {
            const current = timeSeries[i];
            const previous = timeSeries[i - 1];
            
            const absoluteChange = baseline - current.ndvi;
            const relativeChange = (absoluteChange / baseline) * 100;
            
            // Detect significant drops
            if (absoluteChange > alertThreshold) {
                const severity = relativeChange > 50 ? 'HIGH' : 
                               relativeChange > 25 ? 'MEDIUM' : 'LOW';
                
                changes.push({
                    date: current.date,
                    changeType: 'degradation',
                    severity: severity,
                    ndviChange: Math.round(absoluteChange * 1000) / 1000,
                    percentChange: Math.round(relativeChange * 10) / 10,
                    previousNDVI: previous.ndvi,
                    currentNDVI: current.ndvi
                });
            }
        }
        
        return changes;
    }

    /**
     * Generate color scale for NDVI visualization
     */
    getNDVIColor(ndviValue) {
        // Red to Green color scale based on NDVI value
        if (ndviValue < 0.1) return '#8B4513'; // Brown (bare soil)
        if (ndviValue < 0.3) return '#FF6B6B'; // Red (critical)
        if (ndviValue < 0.5) return '#FFD93D'; // Yellow (alert)
        if (ndviValue < 0.7) return '#6BCF7F'; // Light green (moderate)
        return '#2E7D32'; // Dark green (healthy)
    }

    /**
     * Create NDVI visualization overlay data
     */
    createVisualizationData(timeSeries, canvasWidth = 200, canvasHeight = 200) {
        const canvas = document.createElement('canvas');
        canvas.width = canvasWidth;
        canvas.height = canvasHeight;
        const ctx = canvas.getContext('2d');
        
        // Create gradient based on latest NDVI values
        const latestNDVI = timeSeries[timeSeries.length - 1]?.ndvi || 0.5;
        const color = this.getNDVIColor(latestNDVI);
        
        // Fill with semi-transparent color
        ctx.fillStyle = color.replace(')', ', 0.7)').replace('#', 'rgba(') || `rgba(76, 175, 80, 0.7)`;
        ctx.fillRect(0, 0, canvasWidth, canvasHeight);
        
        // Add texture for deforested areas
        if (latestNDVI < this.ALERT_THRESHOLD) {
            this.addDeforestationPattern(ctx, canvasWidth, canvasHeight);
        }
        
        return canvas.toDataURL();
    }

    /**
     * Add deforestation pattern to canvas
     */
    addDeforestationPattern(ctx, width, height) {
        ctx.fillStyle = 'rgba(244, 67, 54, 0.8)';
        
        // Create scattered deforestation patches
        const patches = [
            { x: width * 0.3, y: height * 0.4, w: width * 0.4, h: height * 0.2 },
            { x: width * 0.6, y: height * 0.7, w: width * 0.2, h: height * 0.15 },
            { x: width * 0.15, y: height * 0.75, w: width * 0.25, h: height * 0.125 }
        ];
        
        patches.forEach(patch => {
            ctx.fillRect(patch.x, patch.y, patch.w, patch.h);
        });
    }

    /**
     * Export analysis results for external use
     */
    exportAnalysis(timeSeries, changes, options = {}) {
        const analysis = {
            metadata: {
                generatedAt: new Date().toISOString(),
                analysisType: 'NDVI_Trend_Analysis',
                version: '1.0',
                source: 'FRA_Atlas_MVP'
            },
            summary: {
                totalDataPoints: timeSeries.length,
                dateRange: {
                    start: timeSeries[0]?.date,
                    end: timeSeries[timeSeries.length - 1]?.date
                },
                ndviRange: {
                    min: Math.min(...timeSeries.map(t => t.ndvi)),
                    max: Math.max(...timeSeries.map(t => t.ndvi)),
                    baseline: timeSeries[0]?.ndvi,
                    current: timeSeries[timeSeries.length - 1]?.ndvi
                },
                alertsGenerated: changes.length,
                healthStatus: this.classifyNDVI(timeSeries[timeSeries.length - 1]?.ndvi)
            },
            timeSeries: timeSeries,
            detectedChanges: changes,
            thresholds: {
                healthy: this.HEALTHY_THRESHOLD,
                alert: this.ALERT_THRESHOLD,
                critical: this.CRITICAL_THRESHOLD
            }
        };
        
        if (options.downloadJSON) {
            this.downloadJSON(analysis, 'ndvi_analysis.json');
        }
        
        return analysis;
    }

    /**
     * Download data as JSON file
     */
    downloadJSON(data, filename) {
        const blob = new Blob([JSON.stringify(data, null, 2)], 
                             { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// Example usage for browser console testing
if (typeof window !== 'undefined') {
    window.NDVICalculator = NDVICalculator;
    
    // Initialize calculator and add to window for demo
    window.ndviCalc = new NDVICalculator();
    
    console.log('🛰️ NDVI Calculator loaded!');
    console.log('Try: ndviCalc.generateMockTimeSeries("2025-01-01", "2025-09-15")');
}

// Export for Node.js if available
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NDVICalculator;
}
