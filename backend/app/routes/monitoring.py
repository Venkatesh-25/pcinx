"""
Monitoring API Routes
Satellite monitoring and NDVI analysis endpoints
"""

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app import db
from app.models import FRAClaim, MonitoringData, Alert
from app.services.ndvi_processor import NDVIProcessor
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import json

monitoring_bp = Blueprint('monitoring', __name__)
api = Api(monitoring_bp)

class NDVIAnalysisAPI(Resource):
    """GET /api/monitoring/ndvi/<claim_id> - Get NDVI analysis for a claim"""
    
    def get(self, claim_id):
        try:
            claim = FRAClaim.query.filter_by(claim_id=claim_id).first()
            if not claim:
                return {'error': 'Claim not found'}, 404
            
            # Get date range
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            
            if start_date:
                start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            else:
                start_date = datetime.utcnow() - timedelta(days=365)  # Last year
            
            if end_date:
                end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            else:
                end_date = datetime.utcnow()
            
            # Get monitoring data
            monitoring_data = MonitoringData.query.filter(
                MonitoringData.claim_id == claim.id,
                MonitoringData.observation_date >= start_date.date(),
                MonitoringData.observation_date <= end_date.date()
            ).order_by(MonitoringData.observation_date).all()
            
            # Calculate statistics
            ndvi_values = [data.ndvi_mean for data in monitoring_data if data.ndvi_mean is not None]
            
            if not ndvi_values:
                return {
                    'claim_id': claim_id,
                    'message': 'No NDVI data available for the specified period',
                    'period': {
                        'start_date': start_date.isoformat(),
                        'end_date': end_date.isoformat()
                    }
                }, 200
            
            stats = {
                'mean_ndvi': round(sum(ndvi_values) / len(ndvi_values), 3),
                'min_ndvi': round(min(ndvi_values), 3),
                'max_ndvi': round(max(ndvi_values), 3),
                'latest_ndvi': round(ndvi_values[-1], 3),
                'trend': 'improving' if ndvi_values[-1] > ndvi_values[0] else 'degrading',
                'data_points': len(ndvi_values)
            }
            
            # Check for alerts
            alert_threshold = 0.3
            critical_threshold = 0.1
            current_status = 'healthy'
            
            if stats['latest_ndvi'] < critical_threshold:
                current_status = 'critical'
            elif stats['latest_ndvi'] < alert_threshold:
                current_status = 'alert'
            
            result = {
                'claim_id': claim_id,
                'claim_details': {
                    'village_name': claim.village_name,
                    'district': claim.district,
                    'state': claim.state,
                    'area_hectares': claim.area_hectares
                },
                'analysis_period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat()
                },
                'ndvi_statistics': stats,
                'vegetation_status': current_status,
                'thresholds': {
                    'alert_threshold': alert_threshold,
                    'critical_threshold': critical_threshold
                },
                'time_series': [
                    {
                        'date': data.observation_date.isoformat(),
                        'ndvi_mean': data.ndvi_mean,
                        'ndvi_min': data.ndvi_min,
                        'ndvi_max': data.ndvi_max,
                        'satellite_source': data.satellite_source,
                        'cloud_cover': data.cloud_cover_percentage
                    }
                    for data in monitoring_data
                ]
            }
            
            return result, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

class DeforestationAlertsAPI(Resource):
    """GET /api/monitoring/alerts - Get deforestation alerts"""
    
    def get(self):
        try:
            # Parse query parameters
            severity = request.args.get('severity')  # low, medium, high, critical
            status = request.args.get('status', 'active')
            state = request.args.get('state')
            days = request.args.get('days', 30, type=int)
            
            # Build query
            query = Alert.query.join(FRAClaim)
            
            # Apply filters
            if severity:
                query = query.filter(Alert.severity == severity)
            if status:
                query = query.filter(Alert.status == status)
            if state:
                query = query.filter(FRAClaim.state.ilike(f'%{state}%'))
            
            # Date filter
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            query = query.filter(Alert.detected_at >= cutoff_date)
            
            # Order by severity and date
            severity_order = {
                'critical': 4,
                'high': 3,
                'medium': 2,
                'low': 1
            }
            
            alerts = query.order_by(
                desc(Alert.detected_at)
            ).all()
            
            # Sort by severity (critical first)
            alerts.sort(key=lambda x: severity_order.get(x.severity, 0), reverse=True)
            
            # Prepare response
            result = {
                'alerts': [
                    {
                        **alert.to_dict(),
                        'claim_details': {
                            'claim_id': alert.claim.claim_id,
                            'village_name': alert.claim.village_name,
                            'district': alert.claim.district,
                            'state': alert.claim.state
                        }
                    }
                    for alert in alerts
                ],
                'summary': {
                    'total_alerts': len(alerts),
                    'by_severity': {
                        severity: len([a for a in alerts if a.severity == severity])
                        for severity in ['critical', 'high', 'medium', 'low']
                    },
                    'filters': {
                        'severity': severity,
                        'status': status,
                        'state': state,
                        'days': days
                    }
                }
            }
            
            return result, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

class SatelliteDataAPI(Resource):
    """POST /api/monitoring/satellite - Process new satellite data"""
    
    def post(self):
        try:
            data = request.get_json()
            
            if not data:
                return {'error': 'No data provided'}, 400
            
            required_fields = ['claim_id', 'observation_date', 'ndvi_mean']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return {'error': f'Missing required fields: {missing_fields}'}, 400
            
            # Find the claim
            claim = FRAClaim.query.filter_by(claim_id=data['claim_id']).first()
            if not claim:
                return {'error': 'Claim not found'}, 404
            
            # Create monitoring record
            monitoring_record = MonitoringData(
                claim_id=claim.id,
                observation_date=datetime.fromisoformat(data['observation_date']).date(),
                satellite_source=data.get('satellite_source', 'Sentinel-2'),
                ndvi_mean=data['ndvi_mean'],
                ndvi_min=data.get('ndvi_min'),
                ndvi_max=data.get('ndvi_max'),
                ndvi_std=data.get('ndvi_std'),
                evi_mean=data.get('evi_mean'),
                vegetation_loss_area=data.get('vegetation_loss_area'),
                vegetation_gain_area=data.get('vegetation_gain_area'),
                cloud_cover_percentage=data.get('cloud_cover_percentage'),
                data_quality_score=data.get('data_quality_score'),
                processing_version=data.get('processing_version', '1.0'),
                additional_metrics=data.get('additional_metrics')
            )
            
            db.session.add(monitoring_record)
            
            # Check for alerts
            alert_threshold = 0.3
            critical_threshold = 0.1
            
            if data['ndvi_mean'] < critical_threshold:
                # Create critical alert
                alert = Alert(
                    claim_id=claim.id,
                    alert_type='deforestation',
                    severity='critical',
                    affected_area_hectares=data.get('vegetation_loss_area', 0),
                    confidence_score=0.95,
                    alert_details={
                        'ndvi_value': data['ndvi_mean'],
                        'threshold': critical_threshold,
                        'detection_method': 'NDVI_threshold'
                    }
                )
                db.session.add(alert)
            elif data['ndvi_mean'] < alert_threshold:
                # Create warning alert
                alert = Alert(
                    claim_id=claim.id,
                    alert_type='vegetation_degradation',
                    severity='medium',
                    affected_area_hectares=data.get('vegetation_loss_area', 0),
                    confidence_score=0.85,
                    alert_details={
                        'ndvi_value': data['ndvi_mean'],
                        'threshold': alert_threshold,
                        'detection_method': 'NDVI_threshold'
                    }
                )
                db.session.add(alert)
            
            db.session.commit()
            
            return {
                'message': 'Monitoring data processed successfully',
                'monitoring_id': str(monitoring_record.id),
                'ndvi_status': 'critical' if data['ndvi_mean'] < critical_threshold 
                            else 'alert' if data['ndvi_mean'] < alert_threshold 
                            else 'healthy'
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class VegetationTrendsAPI(Resource):
    """GET /api/monitoring/trends - Get vegetation trends across all claims"""
    
    def get(self):
        try:
            state = request.args.get('state')
            days = request.args.get('days', 90, type=int)
            
            # Date range
            end_date = datetime.utcnow().date()
            start_date = end_date - timedelta(days=days)
            
            # Build base query
            query = db.session.query(
                FRAClaim.state,
                FRAClaim.district,
                func.count(MonitoringData.id).label('monitoring_count'),
                func.avg(MonitoringData.ndvi_mean).label('avg_ndvi'),
                func.min(MonitoringData.ndvi_mean).label('min_ndvi'),
                func.max(MonitoringData.ndvi_mean).label('max_ndvi')
            ).join(MonitoringData).filter(
                MonitoringData.observation_date >= start_date,
                MonitoringData.observation_date <= end_date,
                MonitoringData.ndvi_mean.isnot(None)
            )
            
            if state:
                query = query.filter(FRAClaim.state.ilike(f'%{state}%'))
            
            results = query.group_by(
                FRAClaim.state, FRAClaim.district
            ).all()
            
            # Calculate overall trends
            trends = []
            for state_name, district, count, avg_ndvi, min_ndvi, max_ndvi in results:
                status = 'healthy'
                if avg_ndvi < 0.1:
                    status = 'critical'
                elif avg_ndvi < 0.3:
                    status = 'degraded'
                elif avg_ndvi < 0.5:
                    status = 'moderate'
                
                trends.append({
                    'state': state_name,
                    'district': district,
                    'monitoring_points': int(count),
                    'average_ndvi': round(float(avg_ndvi), 3),
                    'min_ndvi': round(float(min_ndvi), 3),
                    'max_ndvi': round(float(max_ndvi), 3),
                    'vegetation_status': status
                })
            
            # Overall statistics
            all_ndvi_values = db.session.query(MonitoringData.ndvi_mean).filter(
                MonitoringData.observation_date >= start_date,
                MonitoringData.observation_date <= end_date,
                MonitoringData.ndvi_mean.isnot(None)
            ).all()
            
            ndvi_values = [float(val[0]) for val in all_ndvi_values]
            
            summary = {
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'days': days
                },
                'overall_statistics': {
                    'total_monitoring_points': len(ndvi_values),
                    'average_ndvi': round(sum(ndvi_values) / len(ndvi_values), 3) if ndvi_values else 0,
                    'healthy_areas': len([v for v in ndvi_values if v >= 0.5]),
                    'degraded_areas': len([v for v in ndvi_values if 0.3 <= v < 0.5]),
                    'critical_areas': len([v for v in ndvi_values if v < 0.3])
                },
                'regional_trends': trends
            }
            
            return summary, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

# Register API resources
api.add_resource(NDVIAnalysisAPI, '/ndvi/<string:claim_id>')
api.add_resource(DeforestationAlertsAPI, '/alerts')
api.add_resource(SatelliteDataAPI, '/satellite')
api.add_resource(VegetationTrendsAPI, '/trends')