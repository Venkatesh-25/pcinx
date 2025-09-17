"""
Alerts API Routes
Alert management and notification endpoints
"""

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from app import db
from app.models import FRAClaim, Alert
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import json

alerts_bp = Blueprint('alerts', __name__)
api = Api(alerts_bp)

class AlertsListAPI(Resource):
    """GET /api/alerts - List all alerts with filtering"""
    
    def get(self):
        try:
            # Parse query parameters
            severity = request.args.get('severity')
            status = request.args.get('status', 'active')
            alert_type = request.args.get('type')
            state = request.args.get('state')
            days = request.args.get('days', 30, type=int)
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 50, type=int), 100)
            
            # Build query
            query = Alert.query.join(FRAClaim)
            
            # Apply filters
            if severity:
                query = query.filter(Alert.severity == severity)
            if status:
                query = query.filter(Alert.status == status)
            if alert_type:
                query = query.filter(Alert.alert_type == alert_type)
            if state:
                query = query.filter(FRAClaim.state.ilike(f'%{state}%'))
            
            # Date filter
            if days:
                cutoff_date = datetime.utcnow() - timedelta(days=days)
                query = query.filter(Alert.detected_at >= cutoff_date)
            
            # Order by severity and detection time
            severity_order = func.case(
                (Alert.severity == 'critical', 4),
                (Alert.severity == 'high', 3),
                (Alert.severity == 'medium', 2),
                (Alert.severity == 'low', 1),
                else_=0
            )
            
            query = query.order_by(desc(severity_order), desc(Alert.detected_at))
            
            # Paginate
            alerts = query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            # Prepare response
            result = {
                'alerts': [
                    {
                        **alert.to_dict(),
                        'claim_details': {
                            'claim_id': alert.claim.claim_id,
                            'village_name': alert.claim.village_name,
                            'district': alert.claim.district,
                            'state': alert.claim.state,
                            'area_hectares': alert.claim.area_hectares
                        }
                    }
                    for alert in alerts.items
                ],
                'pagination': {
                    'page': page,
                    'pages': alerts.pages,
                    'per_page': per_page,
                    'total': alerts.total,
                    'has_next': alerts.has_next,
                    'has_prev': alerts.has_prev
                },
                'summary': {
                    'total_alerts': alerts.total,
                    'filters_applied': {
                        'severity': severity,
                        'status': status,
                        'type': alert_type,
                        'state': state,
                        'days': days
                    }
                }
            }
            
            return result, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

class AlertCreateAPI(Resource):
    """POST /api/alerts - Create new alert"""
    
    def post(self):
        try:
            data = request.get_json()
            
            if not data:
                return {'error': 'No data provided'}, 400
            
            required_fields = ['claim_id', 'alert_type', 'severity']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return {'error': f'Missing required fields: {missing_fields}'}, 400
            
            # Validate claim exists
            claim = FRAClaim.query.filter_by(claim_id=data['claim_id']).first()
            if not claim:
                return {'error': 'Claim not found'}, 404
            
            # Validate severity
            valid_severities = ['low', 'medium', 'high', 'critical']
            if data['severity'] not in valid_severities:
                return {'error': f'Invalid severity. Must be one of: {valid_severities}'}, 400
            
            # Create alert
            alert = Alert(
                claim_id=claim.id,
                alert_type=data['alert_type'],
                severity=data['severity'],
                affected_area_hectares=data.get('affected_area_hectares'),
                confidence_score=data.get('confidence_score', 0.8),
                alert_details=data.get('alert_details', {})
            )
            
            db.session.add(alert)
            db.session.commit()
            
            return {
                'message': 'Alert created successfully',
                'alert_id': str(alert.id),
                'alert': alert.to_dict()
            }, 201
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class AlertUpdateAPI(Resource):
    """PUT /api/alerts/<alert_id> - Update alert status"""
    
    def put(self, alert_id):
        try:
            alert = Alert.query.get(alert_id)
            if not alert:
                return {'error': 'Alert not found'}, 404
            
            data = request.get_json()
            if not data:
                return {'error': 'No data provided'}, 400
            
            # Update allowed fields
            if 'status' in data:
                valid_statuses = ['active', 'resolved', 'false_positive']
                if data['status'] not in valid_statuses:
                    return {'error': f'Invalid status. Must be one of: {valid_statuses}'}, 400
                alert.status = data['status']
                
                if data['status'] == 'resolved':
                    alert.resolution_date = datetime.utcnow()
                    alert.resolution_notes = data.get('resolution_notes')
            
            if 'reported_to_authorities' in data:
                alert.reported_to_authorities = data['reported_to_authorities']
                if data['reported_to_authorities']:
                    alert.authority_response_date = datetime.utcnow()
            
            if 'resolution_notes' in data:
                alert.resolution_notes = data['resolution_notes']
            
            db.session.commit()
            
            return {
                'message': 'Alert updated successfully',
                'alert': alert.to_dict()
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class AlertStatsAPI(Resource):
    """GET /api/alerts/statistics - Alert statistics and trends"""
    
    def get(self):
        try:
            days = request.args.get('days', 30, type=int)
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Overall alert statistics
            total_alerts = Alert.query.count()
            active_alerts = Alert.query.filter_by(status='active').count()
            resolved_alerts = Alert.query.filter_by(status='resolved').count()
            
            # Recent alerts
            recent_alerts = Alert.query.filter(
                Alert.detected_at >= cutoff_date
            ).count()
            
            # Severity breakdown
            severity_stats = db.session.query(
                Alert.severity,
                func.count(Alert.id).label('count')
            ).filter(Alert.status == 'active').group_by(Alert.severity).all()
            
            # Type breakdown
            type_stats = db.session.query(
                Alert.alert_type,
                func.count(Alert.id).label('count')
            ).filter(Alert.status == 'active').group_by(Alert.alert_type).all()
            
            # State-wise alerts
            state_stats = db.session.query(
                FRAClaim.state,
                func.count(Alert.id).label('alert_count')
            ).join(Alert).filter(
                Alert.status == 'active'
            ).group_by(FRAClaim.state).all()
            
            # Response time analysis
            resolved_with_response = Alert.query.filter(
                Alert.status == 'resolved',
                Alert.authority_response_date.isnot(None),
                Alert.detected_at.isnot(None)
            ).all()
            
            response_times = []
            for alert in resolved_with_response:
                response_time = (alert.authority_response_date - alert.detected_at).total_seconds() / 3600  # hours
                response_times.append(response_time)
            
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            # Critical alerts requiring immediate attention
            critical_alerts = Alert.query.filter(
                Alert.status == 'active',
                Alert.severity == 'critical',
                Alert.reported_to_authorities == False
            ).count()
            
            result = {
                'overview': {
                    'total_alerts': total_alerts,
                    'active_alerts': active_alerts,
                    'resolved_alerts': resolved_alerts,
                    'recent_alerts': recent_alerts,
                    'resolution_rate': round((resolved_alerts / total_alerts * 100), 1) if total_alerts > 0 else 0
                },
                'severity_breakdown': {
                    severity: int(count) for severity, count in severity_stats
                },
                'type_breakdown': {
                    alert_type: int(count) for alert_type, count in type_stats
                },
                'state_distribution': [
                    {
                        'state': state,
                        'alert_count': int(count)
                    }
                    for state, count in state_stats
                ],
                'response_metrics': {
                    'average_response_time_hours': round(avg_response_time, 2),
                    'critical_alerts_pending': critical_alerts,
                    'total_resolved_alerts': len(resolved_with_response)
                },
                'urgent_attention': {
                    'critical_unreported': critical_alerts,
                    'requires_immediate_action': critical_alerts > 0
                },
                'period': {
                    'days': days,
                    'start_date': cutoff_date.isoformat(),
                    'end_date': datetime.utcnow().isoformat()
                }
            }
            
            return result, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

# Register API resources
api.add_resource(AlertsListAPI, '/')
api.add_resource(AlertCreateAPI, '/create')
api.add_resource(AlertUpdateAPI, '/<string:alert_id>')
api.add_resource(AlertStatsAPI, '/statistics')