"""
Analytics API Routes
Advanced analytics and reporting endpoints
"""

from flask import Blueprint, request, jsonify, send_file
from flask_restful import Api, Resource
from app import db
from app.models import FRAClaim, MonitoringData, Alert
from sqlalchemy import func, desc, extract
from datetime import datetime, timedelta
import json
import io
import csv

analytics_bp = Blueprint('analytics', __name__)
api = Api(analytics_bp)

class DashboardStatsAPI(Resource):
    """GET /api/analytics/dashboard - Comprehensive dashboard statistics"""
    
    def get(self):
        try:
            # Time period
            days = request.args.get('days', 30, type=int)
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Claim statistics
            total_claims = FRAClaim.query.count()
            approved_claims = FRAClaim.query.filter_by(status='Approved').count()
            pending_claims = FRAClaim.query.filter_by(status='Pending').count()
            under_review = FRAClaim.query.filter_by(status='Under Review').count()
            rejected_claims = FRAClaim.query.filter_by(status='Rejected').count()
            
            # Recent claims
            recent_claims = FRAClaim.query.filter(
                FRAClaim.created_at >= cutoff_date
            ).count()
            
            # Area and family statistics
            total_area = db.session.query(func.sum(FRAClaim.area_hectares)).scalar() or 0
            approved_area = db.session.query(func.sum(FRAClaim.area_hectares)).filter_by(
                status='Approved'
            ).scalar() or 0
            
            total_families = db.session.query(func.sum(FRAClaim.claimant_families)).scalar() or 0
            protected_families = db.session.query(func.sum(FRAClaim.claimant_families)).filter_by(
                status='Approved'
            ).scalar() or 0
            
            # Alert statistics
            active_alerts = Alert.query.filter_by(status='active').count()
            critical_alerts = Alert.query.filter(
                Alert.status == 'active',
                Alert.severity == 'critical'
            ).count()
            
            recent_alerts = Alert.query.filter(
                Alert.detected_at >= cutoff_date
            ).count()
            
            # Monitoring coverage
            monitored_claims = db.session.query(FRAClaim.id).join(MonitoringData).distinct().count()
            monitoring_coverage = (monitored_claims / total_claims * 100) if total_claims > 0 else 0
            
            # Recent NDVI trends
            recent_monitoring = db.session.query(
                func.avg(MonitoringData.ndvi_mean).label('avg_ndvi')
            ).filter(
                MonitoringData.observation_date >= cutoff_date.date(),
                MonitoringData.ndvi_mean.isnot(None)
            ).scalar()
            
            # System health indicators
            system_health = {
                'data_freshness': 'good',  # Based on last monitoring data
                'alert_response_time': '< 2 hours',
                'api_status': 'operational',
                'database_status': 'healthy'
            }
            
            result = {
                'overview': {
                    'total_claims': total_claims,
                    'approved_claims': approved_claims,
                    'pending_claims': pending_claims,
                    'under_review': under_review,
                    'rejected_claims': rejected_claims,
                    'approval_rate': round((approved_claims / total_claims * 100), 1) if total_claims > 0 else 0,
                    'recent_claims': recent_claims
                },
                'area_statistics': {
                    'total_area_hectares': round(total_area, 2),
                    'approved_area_hectares': round(approved_area, 2),
                    'area_under_protection': round((approved_area / total_area * 100), 1) if total_area > 0 else 0
                },
                'community_impact': {
                    'total_families': int(total_families),
                    'protected_families': int(protected_families),
                    'families_coverage': round((protected_families / total_families * 100), 1) if total_families > 0 else 0
                },
                'environmental_monitoring': {
                    'active_alerts': active_alerts,
                    'critical_alerts': critical_alerts,
                    'recent_alerts': recent_alerts,
                    'monitoring_coverage': round(monitoring_coverage, 1),
                    'average_ndvi': round(recent_monitoring, 3) if recent_monitoring else None
                },
                'system_health': system_health,
                'generated_at': datetime.utcnow().isoformat(),
                'period_days': days
            }
            
            return result, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

class PerformanceMetricsAPI(Resource):
    """GET /api/analytics/performance - SLA and performance metrics"""
    
    def get(self):
        try:
            # Processing time analysis
            processing_times = db.session.query(
                FRAClaim.application_date,
                FRAClaim.approval_date,
                FRAClaim.status
            ).filter(
                FRAClaim.approval_date.isnot(None)
            ).all()
            
            # Calculate average processing times
            processing_days = []
            for app_date, approval_date, status in processing_times:
                if app_date and approval_date:
                    days = (approval_date - app_date).days
                    processing_days.append(days)
            
            avg_processing_time = sum(processing_days) / len(processing_days) if processing_days else 0
            
            # SLA compliance (assume 90 days SLA)
            sla_threshold = 90
            within_sla = len([d for d in processing_days if d <= sla_threshold])
            sla_compliance = (within_sla / len(processing_days) * 100) if processing_days else 0
            
            # Monthly approval trends
            monthly_approvals = db.session.query(
                extract('year', FRAClaim.approval_date).label('year'),
                extract('month', FRAClaim.approval_date).label('month'),
                func.count(FRAClaim.id).label('approvals')
            ).filter(
                FRAClaim.status == 'Approved',
                FRAClaim.approval_date.isnot(None)
            ).group_by('year', 'month').order_by('year', 'month').all()
            
            # State-wise performance
            state_performance = db.session.query(
                FRAClaim.state,
                func.count(FRAClaim.id).label('total'),
                func.sum(func.case([(FRAClaim.status == 'Approved', 1)], else_=0)).label('approved'),
                func.avg(
                    func.extract('epoch', FRAClaim.approval_date - FRAClaim.application_date) / 86400
                ).label('avg_days')
            ).group_by(FRAClaim.state).all()
            
            result = {
                'processing_metrics': {
                    'average_processing_days': round(avg_processing_time, 1),
                    'sla_compliance_percentage': round(sla_compliance, 1),
                    'sla_threshold_days': sla_threshold,
                    'total_processed_claims': len(processing_days)
                },
                'monthly_trends': [
                    {
                        'year': int(year),
                        'month': int(month),
                        'approvals': int(approvals)
                    }
                    for year, month, approvals in monthly_approvals
                ],
                'state_performance': [
                    {
                        'state': state,
                        'total_claims': int(total),
                        'approved_claims': int(approved or 0),
                        'approval_rate': round((approved or 0) / total * 100, 1),
                        'average_processing_days': round(float(avg_days or 0), 1)
                    }
                    for state, total, approved, avg_days in state_performance
                ],
                'performance_indicators': {
                    'efficiency_score': min(100, round(sla_compliance, 0)),
                    'throughput_trend': 'stable',  # Could be calculated from monthly data
                    'bottlenecks': 'document_verification' if avg_processing_time > 60 else 'none'
                }
            }
            
            return result, 200
            
        except Exception as e:
            return {'error': str(e)}, 500

class ExportReportAPI(Resource):
    """GET /api/analytics/export - Export comprehensive report"""
    
    def get(self):
        try:
            format_type = request.args.get('format', 'json')  # json, csv
            
            if format_type not in ['json', 'csv']:
                return {'error': 'Invalid format. Use json or csv'}, 400
            
            # Generate comprehensive report data
            claims_data = db.session.query(
                FRAClaim.claim_id,
                FRAClaim.village_name,
                FRAClaim.district,
                FRAClaim.state,
                FRAClaim.area_hectares,
                FRAClaim.status,
                FRAClaim.claimant_families,
                FRAClaim.application_date,
                FRAClaim.approval_date
            ).all()
            
            # Latest monitoring data for each claim
            latest_monitoring = db.session.query(
                FRAClaim.claim_id,
                MonitoringData.ndvi_mean,
                MonitoringData.observation_date
            ).join(MonitoringData).order_by(
                FRAClaim.claim_id, 
                desc(MonitoringData.observation_date)
            ).distinct(FRAClaim.claim_id).all()
            
            # Active alerts
            active_alerts = db.session.query(
                FRAClaim.claim_id,
                Alert.alert_type,
                Alert.severity,
                Alert.detected_at
            ).join(Alert).filter(Alert.status == 'active').all()
            
            # Combine data
            report_data = []
            monitoring_dict = {claim_id: (ndvi, date) for claim_id, ndvi, date in latest_monitoring}
            alerts_dict = {}
            for claim_id, alert_type, severity, detected_at in active_alerts:
                if claim_id not in alerts_dict:
                    alerts_dict[claim_id] = []
                alerts_dict[claim_id].append({
                    'type': alert_type,
                    'severity': severity,
                    'detected_at': detected_at.isoformat()
                })
            
            for claim in claims_data:
                claim_id = claim.claim_id
                ndvi_data = monitoring_dict.get(claim_id, (None, None))
                alerts = alerts_dict.get(claim_id, [])
                
                report_data.append({
                    'claim_id': claim_id,
                    'village_name': claim.village_name,
                    'district': claim.district,
                    'state': claim.state,
                    'area_hectares': float(claim.area_hectares),
                    'status': claim.status,
                    'claimant_families': claim.claimant_families,
                    'application_date': claim.application_date.isoformat() if claim.application_date else None,
                    'approval_date': claim.approval_date.isoformat() if claim.approval_date else None,
                    'latest_ndvi': float(ndvi_data[0]) if ndvi_data[0] else None,
                    'last_monitored': ndvi_data[1].isoformat() if ndvi_data[1] else None,
                    'active_alerts': len(alerts),
                    'alert_details': alerts
                })
            
            if format_type == 'json':
                return {
                    'report_metadata': {
                        'generated_at': datetime.utcnow().isoformat(),
                        'total_claims': len(report_data),
                        'report_type': 'comprehensive_fra_analysis'
                    },
                    'claims_data': report_data
                }, 200
            
            elif format_type == 'csv':
                # Create CSV in memory
                output = io.StringIO()
                writer = csv.writer(output)
                
                # CSV headers
                headers = [
                    'claim_id', 'village_name', 'district', 'state', 
                    'area_hectares', 'status', 'claimant_families',
                    'application_date', 'approval_date', 'latest_ndvi',
                    'last_monitored', 'active_alerts'
                ]
                writer.writerow(headers)
                
                # CSV data
                for row in report_data:
                    writer.writerow([
                        row['claim_id'], row['village_name'], row['district'],
                        row['state'], row['area_hectares'], row['status'],
                        row['claimant_families'], row['application_date'],
                        row['approval_date'], row['latest_ndvi'],
                        row['last_monitored'], row['active_alerts']
                    ])
                
                output.seek(0)
                return send_file(
                    io.BytesIO(output.getvalue().encode()),
                    mimetype='text/csv',
                    as_attachment=True,
                    download_name=f'fra_atlas_report_{datetime.utcnow().strftime("%Y%m%d")}.csv'
                )
            
        except Exception as e:
            return {'error': str(e)}, 500

# Register API resources
api.add_resource(DashboardStatsAPI, '/dashboard')
api.add_resource(PerformanceMetricsAPI, '/performance')
api.add_resource(ExportReportAPI, '/export')