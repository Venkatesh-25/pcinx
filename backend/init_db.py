"""
Database initialization and migration script
Run this to set up the PostgreSQL database with PostGIS extensions
"""

import os
import sys
from flask import Flask
from flask_migrate import init, migrate, upgrade
from app import create_app, db
from config.settings import Config

def init_database():
    """Initialize database with PostGIS extensions and tables"""
    
    print("🗃️ Initializing FRA Atlas DSS Database...")
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Enable PostGIS extension (requires superuser privileges)
            print("🌍 Enabling PostGIS extension...")
            db.engine.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
            db.engine.execute("CREATE EXTENSION IF NOT EXISTS postgis_topology;")
            print("✅ PostGIS extensions enabled")
            
            # Create spatial indexes
            print("📍 Creating spatial indexes...")
            db.engine.execute("""
                CREATE INDEX IF NOT EXISTS idx_fra_claims_geometry 
                ON fra_claims USING GIST (geometry);
            """)
            db.engine.execute("""
                CREATE INDEX IF NOT EXISTS idx_alerts_geometry 
                ON alerts USING GIST (alert_geometry);
            """)
            print("✅ Spatial indexes created")
            
            print("🎉 Database initialization completed successfully!")
            
        except Exception as e:
            print(f"❌ Error initializing database: {str(e)}")
            sys.exit(1)

def load_sample_data():
    """Load sample FRA claims data from GeoJSON files"""
    
    import json
    import uuid
    from datetime import datetime, date
    from app.models import FRAClaim, MonitoringData, Alert
    from geoalchemy2.shape import from_shape
    from shapely.geometry import shape
    
    print("📊 Loading sample data...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Sample data files
            data_files = [
                ('assets/data/odisha-claims.geojson', 'Odisha'),
                ('assets/data/mp-claims.geojson', 'Madhya Pradesh'),
                ('assets/data/tripura-claims.geojson', 'Tripura'),
                ('assets/data/telangana-claims.geojson', 'Telangana')
            ]
            
            total_claims = 0
            
            for file_path, state_name in data_files:
                full_path = os.path.join('..', '..', file_path)
                
                if not os.path.exists(full_path):
                    print(f"⚠️ Sample data file not found: {full_path}")
                    continue
                
                print(f"Loading {state_name} claims from {file_path}...")
                
                with open(full_path, 'r') as f:
                    geojson_data = json.load(f)
                
                for feature in geojson_data['features']:
                    props = feature['properties']
                    geometry = feature['geometry']
                    
                    # Create FRA claim
                    claim = FRAClaim(
                        id=uuid.uuid4(),
                        claim_id=props['claim_id'],
                        village_name=props['village_name'],
                        district=props['district'],
                        state=props['state'],
                        area_hectares=props['area_hectares'],
                        status=props['status'],
                        rights_type=props.get('rights_type', 'Community Forest Rights'),
                        forest_type=props.get('forest_type', 'Reserved Forest'),
                        claimant_families=props.get('claimant_families', 1),
                        application_date=datetime.fromisoformat(props['application_date']) if props.get('application_date') else datetime.utcnow(),
                        approval_date=datetime.fromisoformat(props['approval_date']) if props.get('approval_date') else None,
                        survey_number=props.get('survey_number'),
                        gps_surveyed=props.get('gps_surveyed', False),
                        geometry=from_shape(shape(geometry)),
                        created_at=datetime.utcnow()
                    )
                    
                    db.session.add(claim)
                    
                    # Add sample monitoring data
                    if props.get('ndvi_baseline'):
                        monitoring = MonitoringData(
                            id=uuid.uuid4(),
                            claim_id=claim.id,
                            observation_date=date.today(),
                            satellite_source='Sentinel-2',
                            ndvi_mean=props['ndvi_baseline'],
                            cloud_cover_percentage=10.0,
                            data_quality_score=0.95,
                            processing_version='1.0'
                        )
                        db.session.add(monitoring)
                        
                        # Create alert if NDVI is low
                        if props['ndvi_baseline'] < 0.3:
                            alert = Alert(
                                id=uuid.uuid4(),
                                claim_id=claim.id,
                                alert_type='deforestation',
                                severity='high' if props['ndvi_baseline'] < 0.1 else 'medium',
                                confidence_score=0.85,
                                alert_details={
                                    'ndvi_value': props['ndvi_baseline'],
                                    'detection_method': 'baseline_analysis'
                                }
                            )
                            db.session.add(alert)
                    
                    total_claims += 1
            
            # Commit all changes
            db.session.commit()
            print(f"✅ Successfully loaded {total_claims} FRA claims with monitoring data")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error loading sample data: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "load-data":
        load_sample_data()
    else:
        init_database()