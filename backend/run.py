"""
FRA Atlas DSS - Main Application Entry Point
Production-ready Flask application for Smart India Hackathon 2025
"""

import os
from app import create_app, db
from app.models import FRAClaim, MonitoringData, Alert
from config.settings import config

# Create Flask application
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config[config_name])

@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    return {
        'db': db,
        'FRAClaim': FRAClaim,
        'MonitoringData': MonitoringData,
        'Alert': Alert
    }

@app.cli.command()
def init_db():
    """Initialize database with tables and PostGIS extensions"""
    from init_db import init_database
    init_database()

@app.cli.command()
def load_sample_data():
    """Load sample FRA claims data"""
    from init_db import load_sample_data
    load_sample_data()

@app.cli.command()
def create_test_data():
    """Create test data for development"""
    from datetime import datetime, date, timedelta
    import uuid
    import random
    
    with app.app_context():
        print("Creating test data...")
        
        # Sample states and districts
        locations = [
            ('Odisha', 'Kendrapada'),
            ('Odisha', 'Mayurbhanj'),
            ('Madhya Pradesh', 'Hoshangabad'),
            ('Madhya Pradesh', 'Betul'),
            ('Tripura', 'West Tripura'),
            ('Telangana', 'Adilabad')
        ]
        
        statuses = ['Approved', 'Pending', 'Under Review', 'Rejected']
        rights_types = ['Individual Forest Rights', 'Community Forest Rights']
        
        for i in range(20):  # Create 20 test claims
            state, district = random.choice(locations)
            
            claim = FRAClaim(
                id=uuid.uuid4(),
                claim_id=f'CFR-2024-{state[:2].upper()}-{i+1:03d}',
                village_name=f'Test Village {i+1}',
                district=district,
                state=state,
                area_hectares=round(random.uniform(10, 500), 2),
                status=random.choice(statuses),
                rights_type=random.choice(rights_types),
                claimant_families=random.randint(1, 50),
                application_date=datetime.utcnow() - timedelta(days=random.randint(30, 365)),
                gps_surveyed=random.choice([True, False]),
                created_at=datetime.utcnow()
            )
            
            db.session.add(claim)
            
            # Add monitoring data
            for j in range(random.randint(5, 15)):
                obs_date = date.today() - timedelta(days=random.randint(1, 365))
                ndvi_val = round(random.uniform(0.1, 0.8), 3)
                
                monitoring = MonitoringData(
                    id=uuid.uuid4(),
                    claim_id=claim.id,
                    observation_date=obs_date,
                    satellite_source='Sentinel-2',
                    ndvi_mean=ndvi_val,
                    ndvi_min=max(0, ndvi_val - 0.1),
                    ndvi_max=min(1, ndvi_val + 0.1),
                    cloud_cover_percentage=random.uniform(0, 30),
                    data_quality_score=random.uniform(0.8, 1.0),
                    processing_version='1.0'
                )
                db.session.add(monitoring)
                
                # Create alerts for low NDVI
                if ndvi_val < 0.3 and random.random() < 0.5:
                    alert = Alert(
                        id=uuid.uuid4(),
                        claim_id=claim.id,
                        alert_type=random.choice(['deforestation', 'vegetation_degradation']),
                        severity='critical' if ndvi_val < 0.15 else 'high',
                        confidence_score=random.uniform(0.7, 0.95),
                        detected_at=datetime.combine(obs_date, datetime.min.time())
                    )
                    db.session.add(alert)
        
        db.session.commit()
        print("✅ Test data created successfully!")

if __name__ == '__main__':
    # Development server
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    )