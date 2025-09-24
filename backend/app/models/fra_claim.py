from app import db
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import func
from datetime import datetime
import uuid

class FRAClaim(db.Model):
    __tablename__ = 'fra_claims'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    village_name = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    block = db.Column(db.String(100))
    tehsil = db.Column(db.String(100))
    
    area_hectares = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), nullable=False, default='Pending')
    rights_type = db.Column(db.String(50), nullable=False)
    forest_type = db.Column(db.String(50))
    
    claimant_families = db.Column(db.Integer, default=1)
    claimant_name = db.Column(db.String(200))
    contact_number = db.Column(db.String(15))
    
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    approval_date = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    survey_number = db.Column(db.String(50))
    gps_surveyed = db.Column(db.Boolean, default=False)
    documents_verified = db.Column(db.Boolean, default=False)
    
    geometry = db.Column(Geometry('POLYGON', srid=4326))
    centroid = db.Column(Geometry('POINT', srid=4326))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.String(100))
    metadata = db.Column(JSONB)
    
    monitoring_data = db.relationship('MonitoringData', backref='claim', lazy='dynamic')
    alerts = db.relationship('Alert', backref='claim', lazy='dynamic')
    
    def __repr__(self):
        return f'<FRAClaim {self.claim_id}: {self.village_name}, {self.district}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'claim_id': self.claim_id,
            'village_name': self.village_name,
            'district': self.district,
            'state': self.state,
            'area_hectares': self.area_hectares,
            'status': self.status,
            'rights_type': self.rights_type,
            'claimant_families': self.claimant_families,
            'application_date': self.application_date.isoformat() if self.application_date else None,
            'approval_date': self.approval_date.isoformat() if self.approval_date else None,
            'gps_surveyed': self.gps_surveyed,
            'created_at': self.created_at.isoformat(),
        }
    
    def to_geojson_feature(self):
        return {
            'type': 'Feature',
            'properties': self.to_dict(),
            'geometry': {
                'type': 'Polygon',
                'coordinates': []
            }
        }

class MonitoringData(db.Model):
    __tablename__ = 'monitoring_data'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = db.Column(UUID(as_uuid=True), db.ForeignKey('fra_claims.id'), nullable=False)
    
    observation_date = db.Column(db.Date, nullable=False)
    satellite_source = db.Column(db.String(50), default='Sentinel-2')
    
    ndvi_mean = db.Column(db.Float)
    ndvi_min = db.Column(db.Float)
    ndvi_max = db.Column(db.Float)
    ndvi_std = db.Column(db.Float)
    
    evi_mean = db.Column(db.Float)
    savi_mean = db.Column(db.Float)
    
    vegetation_loss_area = db.Column(db.Float)
    vegetation_gain_area = db.Column(db.Float)
    
    cloud_cover_percentage = db.Column(db.Float)
    data_quality_score = db.Column(db.Float)
    
    processed_at = db.Column(db.DateTime, default=datetime.utcnow)
    processing_version = db.Column(db.String(20))
    raw_data_path = db.Column(db.String(500))
    
    additional_metrics = db.Column(JSONB)
    
    def __repr__(self):
        return f'<MonitoringData {self.claim.claim_id}: {self.observation_date}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'claim_id': str(self.claim_id),
            'observation_date': self.observation_date.isoformat(),
            'satellite_source': self.satellite_source,
            'ndvi_mean': self.ndvi_mean,
            'vegetation_loss_area': self.vegetation_loss_area,
            'vegetation_gain_area': self.vegetation_gain_area,
            'cloud_cover_percentage': self.cloud_cover_percentage,
            'processed_at': self.processed_at.isoformat()
        }

class Alert(db.Model):
    __tablename__ = 'alerts'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id = db.Column(UUID(as_uuid=True), db.ForeignKey('fra_claims.id'), nullable=False)
    
    alert_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='active')
    
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    affected_area_hectares = db.Column(db.Float)
    confidence_score = db.Column(db.Float)
    
    alert_geometry = db.Column(Geometry('POLYGON', srid=4326))
    
    reported_to_authorities = db.Column(db.Boolean, default=False)
    authority_response_date = db.Column(db.DateTime)
    resolution_date = db.Column(db.DateTime)
    resolution_notes = db.Column(db.Text)
    
    satellite_image_before = db.Column(db.String(500))
    satellite_image_after = db.Column(db.String(500))
    field_report_path = db.Column(db.String(500))
    
    alert_details = db.Column(JSONB)
    
    def __repr__(self):
        return f'<Alert {self.alert_type}: {self.claim.claim_id} - {self.severity}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'claim_id': str(self.claim_id),
            'alert_type': self.alert_type,
            'severity': self.severity,
            'status': self.status,
            'detected_at': self.detected_at.isoformat(),
            'affected_area_hectares': self.affected_area_hectares,
            'confidence_score': self.confidence_score,
            'reported_to_authorities': self.reported_to_authorities
        }

db.Index('idx_fra_claims_status', FRAClaim.status)
db.Index('idx_fra_claims_state_district', FRAClaim.state, FRAClaim.district)
db.Index('idx_fra_claims_geometry', FRAClaim.geometry, postgresql_using='gist')
db.Index('idx_monitoring_date', MonitoringData.observation_date)
db.Index('idx_alerts_type_severity', Alert.alert_type, Alert.severity)
db.Index('idx_alerts_status', Alert.status)
