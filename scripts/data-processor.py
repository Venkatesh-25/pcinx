# 🐍 FRA Atlas DSS - Data Processor
# Future backend component for processing FRA claims and satellite data

import json
import geopandas as gpd
from datetime import datetime, timedelta
import numpy as np

class FRADataProcessor:
    """
    Core data processing engine for FRA Atlas DSS
    Handles claim data validation, NDVI analysis, and alert generation
    """
    
    def __init__(self, config_path="config.json"):
        self.config = self.load_config(config_path)
        self.ndvi_threshold = 0.3  # Deforestation alert threshold
        
    def load_config(self, path):
        """Load configuration from JSON file"""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "sentinel_api_key": "your_api_key",
                "database_url": "postgresql://user:pass@localhost/fra_atlas",
                "alert_email": "alerts@fra-atlas.gov.in"
            }
    
    def process_claim_data(self, geojson_path):
        """
        Process and validate FRA claim GeoJSON data
        Returns: cleaned and validated GeoDataFrame
        """
        try:
            # Load spatial data
            gdf = gpd.read_file(geojson_path)
            
            # Validate required fields
            required_fields = ['claim_id', 'village_name', 'district', 'status']
            missing_fields = [f for f in required_fields if f not in gdf.columns]
            
            if missing_fields:
                print(f"Warning: Missing required fields: {missing_fields}")
            
            # Clean and standardize data
            gdf['claim_id'] = gdf['claim_id'].str.upper()
            gdf['status'] = gdf['status'].str.title()
            gdf['area_hectares'] = gdf.geometry.area / 10000  # Convert to hectares
            
            # Add processing metadata
            gdf['processed_date'] = datetime.now().isoformat()
            gdf['data_source'] = 'FRA_Atlas_MVP'
            
            print(f"Processed {len(gdf)} FRA claims successfully")
            return gdf
            
        except Exception as e:
            print(f"Error processing claim data: {str(e)}")
            return None
    
    def calculate_ndvi_trend(self, claim_geometry, start_date, end_date):
        """
        Calculate NDVI trend for a specific claim area
        This is a mock implementation - real version would use Sentinel-2 API
        """
        # Mock NDVI calculation with realistic trend
        days = (end_date - start_date).days
        date_range = [start_date + timedelta(days=x) for x in range(0, days, 10)]
        
        # Simulate degrading NDVI trend
        baseline_ndvi = 0.75
        degradation_rate = 0.02  # 2% per month
        
        ndvi_values = []
        for i, date in enumerate(date_range):
            months_elapsed = i * 10 / 30  # Approximate months
            current_ndvi = baseline_ndvi - (degradation_rate * months_elapsed)
            
            # Add some realistic noise
            noise = np.random.normal(0, 0.05)
            current_ndvi = max(0.1, min(0.9, current_ndvi + noise))
            
            ndvi_values.append({
                'date': date.isoformat(),
                'ndvi_mean': round(current_ndvi, 3),
                'data_source': 'Sentinel-2_Simulated'
            })
        
        return ndvi_values
    
    def detect_deforestation_alerts(self, ndvi_data):
        """
        Analyze NDVI data and generate deforestation alerts
        """
        alerts = []
        
        if len(ndvi_data) < 2:
            return alerts
        
        # Compare latest NDVI with baseline
        baseline_ndvi = ndvi_data[0]['ndvi_mean']
        latest_ndvi = ndvi_data[-1]['ndvi_mean']
        
        ndvi_drop = baseline_ndvi - latest_ndvi
        drop_percentage = (ndvi_drop / baseline_ndvi) * 100
        
        if latest_ndvi < self.ndvi_threshold:
            severity = "HIGH" if drop_percentage > 50 else "MEDIUM"
            
            alert = {
                'alert_id': f"ALERT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'type': 'deforestation',
                'severity': severity,
                'detected_date': datetime.now().isoformat(),
                'ndvi_baseline': baseline_ndvi,
                'ndvi_current': latest_ndvi,
                'ndvi_drop_percent': round(drop_percentage, 1),
                'confidence_score': 0.85,
                'status': 'OPEN'
            }
            
            alerts.append(alert)
            print(f"🚨 Deforestation alert generated: {severity} severity")
        
        return alerts
    
    def generate_summary_report(self, claims_gdf, alerts_data):
        """
        Generate summary statistics for dashboard
        """
        summary = {
            'total_claims': len(claims_gdf),
            'claims_by_status': claims_gdf['status'].value_counts().to_dict(),
            'total_area_hectares': round(claims_gdf['area_hectares'].sum(), 1),
            'active_alerts': len([a for a in alerts_data if a['status'] == 'OPEN']),
            'alert_breakdown': {},
            'generated_at': datetime.now().isoformat()
        }
        
        # Alert severity breakdown
        for alert in alerts_data:
            severity = alert.get('severity', 'UNKNOWN')
            summary['alert_breakdown'][severity] = summary['alert_breakdown'].get(severity, 0) + 1
        
        return summary
    
    def export_to_json(self, data, output_path):
        """Export processed data to JSON format"""
        try:
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            print(f"Data exported to {output_path}")
        except Exception as e:
            print(f"Error exporting data: {str(e)}")

# Example usage for future implementation
if __name__ == "__main__":
    processor = FRADataProcessor()
    
    # Process sample claims data
    claims_data = processor.process_claim_data("../assets/data/sample-claims.geojson")
    
    if claims_data is not None:
        # Mock NDVI analysis for first claim
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 9, 15)
        
        # Get first claim geometry (in real implementation)
        first_claim = claims_data.iloc[0]
        ndvi_trend = processor.calculate_ndvi_trend(
            first_claim.geometry, start_date, end_date
        )
        
        # Detect alerts
        alerts = processor.detect_deforestation_alerts(ndvi_trend)
        
        # Generate summary
        summary = processor.generate_summary_report(claims_data, alerts)
        
        # Export results
        processor.export_to_json({
            'ndvi_trend': ndvi_trend,
            'alerts': alerts,
            'summary': summary
        }, '../assets/data/processed_analysis.json')
        
        print("\n📊 Processing Complete!")
        print(f"Claims processed: {summary['total_claims']}")
        print(f"Alerts generated: {len(alerts)}")
        print(f"Total area monitored: {summary['total_area_hectares']} hectares")
