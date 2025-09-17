"""
FRA Claims API Routes
RESTful endpoints for FRA claim management
"""

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app import db
from app.models import FRAClaim, MonitoringData
from sqlalchemy import func, and_
from geoalchemy2.functions import ST_AsGeoJSON, ST_Area, ST_Within
import json
from datetime import datetime

claims_bp = Blueprint('claims', __name__)
api = Api(claims_bp)

class ClaimsListAPI(Resource):
    """GET /api/claims - List all FRA claims with filtering and pagination"""
    
    def get(self):
        try:
            # Parse query parameters
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 50, type=int), 100)
            state = request.args.get('state')
            district = request.args.get('district')
            status = request.args.get('status')
            
            # Build query
            query = FRAClaim.query
            
            # Apply filters
            if state:
                query = query.filter(FRAClaim.state.ilike(f'%{state}%'))
            if district:
                query = query.filter(FRAClaim.district.ilike(f'%{district}%'))
            if status:
                query = query.filter(FRAClaim.status == status)
            
            # Execute paginated query
            claims = query.paginate(
                page=page, 
                per_page=per_page, 
                error_out=False
            )
            
            # Prepare response
            result = {
                'claims': [claim.to_dict() for claim in claims.items],
                'pagination': {
                    'page': page,
                    'pages': claims.pages,
                    'per_page': per_page,
                    'total': claims.total,
                    'has_next': claims.has_next,
                    'has_prev': claims.has_prev
                },
                'filters': {
                    'state': state,
                    'district': district,
                    'status': status
                }
            }
            
            return result, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

class ClaimsGeoJSONAPI(Resource):
    """GET /api/claims/geojson - Return claims as GeoJSON FeatureCollection"""
    
    def get(self):
        try:
            # Parse filters
            state = request.args.get('state')
            bbox = request.args.get('bbox')  # format: minlon,minlat,maxlon,maxlat
            
            # Build query with spatial data
            query = db.session.query(
                FRAClaim,
                ST_AsGeoJSON(FRAClaim.geometry).label('geom_json')
            )
            
            if state:
                query = query.filter(FRAClaim.state.ilike(f'%{state}%'))
            
            # Bounding box filter (if provided)
            if bbox:
                try:
                    minlon, minlat, maxlon, maxlat = map(float, bbox.split(','))
                    bbox_geom = f'POLYGON(({minlon} {minlat},{maxlon} {minlat},{maxlon} {maxlat},{minlon} {maxlat},{minlon} {minlat}))'
                    query = query.filter(
                        ST_Within(FRAClaim.geometry, func.ST_GeomFromText(bbox_geom, 4326))
                    )
                except (ValueError, IndexError):
                    return {'error': 'Invalid bbox format. Use: minlon,minlat,maxlon,maxlat'}, 400
            
            results = query.all()
            
            # Build GeoJSON FeatureCollection
            features = []
            for claim, geom_json in results:
                feature = {
                    'type': 'Feature',
                    'properties': claim.to_dict(),
                    'geometry': json.loads(geom_json) if geom_json else None
                }
                features.append(feature)
            
            geojson = {
                'type': 'FeatureCollection',
                'features': features,
                'metadata': {
                    'total_features': len(features),
                    'generated_at': datetime.utcnow().isoformat(),
                    'filters': {
                        'state': state,
                        'bbox': bbox
                    }
                }
            }
            
            return geojson, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

class ClaimDetailAPI(Resource):
    """GET /api/claims/<claim_id> - Get specific claim details"""
    
    def get(self, claim_id):
        try:
            claim = FRAClaim.query.filter_by(claim_id=claim_id).first()
            if not claim:
                return {'error': 'Claim not found'}, 404
            
            # Get recent monitoring data
            recent_monitoring = MonitoringData.query.filter_by(
                claim_id=claim.id
            ).order_by(MonitoringData.observation_date.desc()).limit(10).all()
            
            # Get active alerts
            active_alerts = claim.alerts.filter_by(status='active').all()
            
            result = {
                'claim': claim.to_dict(),
                'monitoring_data': [data.to_dict() for data in recent_monitoring],
                'active_alerts': [alert.to_dict() for alert in active_alerts],
                'statistics': {
                    'total_monitoring_records': claim.monitoring_data.count(),
                    'total_alerts': claim.alerts.count(),
                    'active_alerts': len(active_alerts)
                }
            }
            
            return result, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

class ClaimsStatsAPI(Resource):
    """GET /api/claims/statistics - Aggregate statistics"""
    
    def get(self):
        try:
            # Overall statistics
            total_claims = FRAClaim.query.count()
            approved_claims = FRAClaim.query.filter_by(status='Approved').count()
            pending_claims = FRAClaim.query.filter_by(status='Pending').count()
            under_review = FRAClaim.query.filter_by(status='Under Review').count()
            rejected_claims = FRAClaim.query.filter_by(status='Rejected').count()
            
            # Area statistics
            total_area = db.session.query(func.sum(FRAClaim.area_hectares)).scalar() or 0
            approved_area = db.session.query(func.sum(FRAClaim.area_hectares)).filter_by(
                status='Approved'
            ).scalar() or 0
            
            # Family statistics
            total_families = db.session.query(func.sum(FRAClaim.claimant_families)).scalar() or 0
            protected_families = db.session.query(func.sum(FRAClaim.claimant_families)).filter_by(
                status='Approved'
            ).scalar() or 0
            
            # State-wise breakdown
            state_stats = db.session.query(
                FRAClaim.state,
                func.count(FRAClaim.id).label('claim_count'),
                func.sum(FRAClaim.area_hectares).label('total_area'),
                func.sum(FRAClaim.claimant_families).label('total_families')
            ).group_by(FRAClaim.state).all()
            
            # Status breakdown
            status_stats = db.session.query(
                FRAClaim.status,
                func.count(FRAClaim.id).label('count'),
                func.sum(FRAClaim.area_hectares).label('area')
            ).group_by(FRAClaim.status).all()
            
            result = {
                'overview': {
                    'total_claims': total_claims,
                    'approved_claims': approved_claims,
                    'pending_claims': pending_claims,
                    'under_review': under_review,
                    'rejected_claims': rejected_claims,
                    'approval_rate': round((approved_claims / total_claims * 100), 2) if total_claims > 0 else 0
                },
                'area_statistics': {
                    'total_area_hectares': round(total_area, 2),
                    'approved_area_hectares': round(approved_area, 2),
                    'area_approval_rate': round((approved_area / total_area * 100), 2) if total_area > 0 else 0
                },
                'community_impact': {
                    'total_families': int(total_families),
                    'protected_families': int(protected_families),
                    'families_secured_rate': round((protected_families / total_families * 100), 2) if total_families > 0 else 0
                },
                'state_breakdown': [
                    {
                        'state': state,
                        'claim_count': int(count),
                        'total_area': round(float(area or 0), 2),
                        'total_families': int(families or 0)
                    }
                    for state, count, area, families in state_stats
                ],
                'status_breakdown': [
                    {
                        'status': status,
                        'count': int(count),
                        'area_hectares': round(float(area or 0), 2)
                    }
                    for status, count, area in status_stats
                ]
            }
            
            return result, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

# Register API resources
api.add_resource(ClaimsListAPI, '/')
api.add_resource(ClaimsGeoJSONAPI, '/geojson')
api.add_resource(ClaimDetailAPI, '/<string:claim_id>')
api.add_resource(ClaimsStatsAPI, '/statistics')