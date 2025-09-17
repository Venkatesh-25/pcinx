/**
 * Dashboard Component - Manages statistics and dashboard updates
 */

class Dashboard {
    constructor() {
        this.elements = this.findDashboardElements();
        this.statsCalculator = new window.DataStatsCalculator();
        this.defaultCounts = {
            approved: 234,
            pending: 156,
            review: 43,
            rejected: 12
        };
        
        // Initialize with real stats
        this.initializeRealStats();
    }

    /**
     * Initialize with real statistics from data files
     */
    async initializeRealStats() {
        try {
            const realStats = await this.statsCalculator.calculateRealStats();
            this.updateStatistics({
                approved: realStats.approved,
                pending: realStats.pending,
                review: realStats.review,
                rejected: realStats.rejected
            });
            
            // Update community impact metrics
            this.updateCommunityMetrics(realStats.families_protected, realStats.hectares_secured);
            
            console.log('Real statistics loaded:', realStats);
        } catch (error) {
            console.warn('Using default statistics due to error:', error);
            this.updateStatistics(this.defaultCounts);
        }
    }

    /**
     * Find dashboard DOM elements
     */
    findDashboardElements() {
        return {
            approved: document.getElementById('approved-count'),
            pending: document.getElementById('pending-count'),
            review: document.getElementById('review-count'),
            rejected: document.getElementById('rejected-count'),
            lastUpdate: document.getElementById('last-update'),
            coverage: document.querySelector('.dashboard-section p')
        };
    }

    /**
     * Update dashboard counts from loaded GeoJSON data
     */
    updateFromData(features) {
        const counts = { approved: 0, pending: 0, review: 0, rejected: 0 };
        let totalFamilies = 0;
        let totalArea = 0;
        
        features.forEach(feature => {
            const props = feature.properties;
            const status = (props.status || '').toLowerCase();
            const families = props.claimant_families || 0;
            const area = props.area_hectares || 0;
            
            totalFamilies += families;
            totalArea += area;
            
            if (status.includes('approved')) counts.approved++;
            else if (status.includes('pending')) counts.pending++;
            else if (status.includes('review')) counts.review++;
            else if (status.includes('reject')) counts.rejected++;
        });
        
        this.updateCountElements(counts);
        this.updateLastUpdate();
        this.updateCoverageInfo(features.length);
        
        console.log(`📊 Dashboard updated: ${features.length} claims, ${totalFamilies} families, ${totalArea.toFixed(1)} hectares`);
    }

    /**
     * Update count elements in DOM
     */
    updateCountElements(counts) {
        if (this.elements.approved) {
            this.elements.approved.textContent = counts.approved;
        }
        if (this.elements.pending) {
            this.elements.pending.textContent = counts.pending;
        }
        if (this.elements.review) {
            this.elements.review.textContent = counts.review;
        }
        if (this.elements.rejected) {
            this.elements.rejected.textContent = counts.rejected;
        }
    }

    /**
     * Update last update timestamp
     */
    updateLastUpdate() {
        if (this.elements.lastUpdate) {
            this.elements.lastUpdate.textContent = 'Updated ' + new Date().toLocaleTimeString();
        }
    }

    /**
     * Update coverage information
     */
    updateCoverageInfo(claimCount) {
        if (this.elements.coverage) {
            // Find the coverage text and update it
            const currentText = this.elements.coverage.innerHTML;
            if (currentText.includes('Coverage:')) {
                this.elements.coverage.innerHTML = currentText.replace(
                    /Coverage: \d+ States.*$/,
                    `Coverage: 4 States | ${claimCount} Active Claims`
                );
            }
        }
    }

    /**
     * Reset to default counts (for fallback scenarios)
     */
    resetToDefaults() {
        this.updateCountElements(this.defaultCounts);
        this.updateLastUpdate();
        console.log('📊 Dashboard reset to default values');
    }

    /**
     * Get current statistics for reporting
     */
    getCurrentStats() {
        return {
            approved: parseInt(this.elements.approved?.textContent || '0'),
            pending: parseInt(this.elements.pending?.textContent || '0'),
            review: parseInt(this.elements.review?.textContent || '0'),
            rejected: parseInt(this.elements.rejected?.textContent || '0')
        };
    }

    /**
     * Add alert to dashboard
     */
    addAlert(message, type = 'warning') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle"></i>
            <span>${message}</span>
        `;
        
        // Find dashboard container and prepend alert
        const dashboard = document.querySelector('.dashboard');
        if (dashboard) {
            dashboard.insertBefore(alertDiv, dashboard.firstChild);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.parentNode.removeChild(alertDiv);
                }
            }, 5000);
        }
    }

    /**
     * Update community impact metrics
     */
    updateCommunityMetrics(familiesProtected, hectaresSecured) {
        // Update families protected count
        const familiesElement = document.querySelector('.stat-card .stat-number');
        if (familiesElement && familiesElement.textContent.includes('8,542')) {
            this.animateCount(familiesElement, familiesProtected, 1000);
        }
        
        // Update hectares secured count  
        const hectaresElement = document.querySelector('.stat-card:last-child .stat-number');
        if (hectaresElement && hectaresElement.textContent.includes('24,156')) {
            this.animateCount(hectaresElement, Math.round(hectaresSecured), 1000);
        }
    }

    /**
     * Update system status
     */
    updateSystemStatus(status, message) {
        const statusElements = document.querySelectorAll('.status-item');
        statusElements.forEach(element => {
            if (element.textContent.includes('System Status')) {
                element.innerHTML = `
                    <i class="fas fa-circle" style="color: ${status === 'online' ? '#4CAF50' : '#f44336'}"></i>
                    System Status: ${message}
                `;
            }
        });
    }
}