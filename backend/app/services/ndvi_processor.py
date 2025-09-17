"""
NDVI Processing Service
Advanced satellite data processing and analysis
"""

import numpy as np
from datetime import datetime, timedelta
import json
from typing import List, Dict, Tuple, Optional

class NDVIProcessor:
    """
    NDVI (Normalized Difference Vegetation Index) processing service
    Handles satellite data analysis and vegetation health monitoring
    """
    
    def __init__(self):
        self.HEALTHY_THRESHOLD = 0.6
        self.MODERATE_THRESHOLD = 0.4
        self.ALERT_THRESHOLD = 0.3
        self.CRITICAL_THRESHOLD = 0.1
        
    def calculate_ndvi(self, nir_band: np.ndarray, red_band: np.ndarray) -> np.ndarray:
        """
        Calculate NDVI from Near-Infrared and Red band arrays
        NDVI = (NIR - Red) / (NIR + Red)
        
        Args:
            nir_band: Near-infrared band array
            red_band: Red band array
            
        Returns:
            NDVI array with values between -1 and 1
        """
        # Avoid division by zero
        denominator = nir_band + red_band
        denominator = np.where(denominator == 0, np.nan, denominator)
        
        ndvi = (nir_band - red_band) / denominator
        
        # Clip to valid NDVI range
        ndvi = np.clip(ndvi, -1, 1)
        
        return ndvi
    
    def analyze_vegetation_health(self, ndvi_value: float) -> Dict[str, any]:
        """
        Analyze vegetation health based on NDVI value
        
        Args:
            ndvi_value: NDVI value to analyze
            
        Returns:
            Dictionary with health status and recommendations
        """
        if ndvi_value >= self.HEALTHY_THRESHOLD:
            status = "healthy"
            health_score = 100
            recommendation = "Continue monitoring. Vegetation is in excellent condition."
            
        elif ndvi_value >= self.MODERATE_THRESHOLD:
            status = "moderate"
            health_score = 70
            recommendation = "Monitor closely. Vegetation health is moderate, watch for declining trends."
            
        elif ndvi_value >= self.ALERT_THRESHOLD:
            status = "degraded"
            health_score = 40
            recommendation = "Alert: Vegetation is degraded. Investigate potential causes and implement conservation measures."
            
        elif ndvi_value >= self.CRITICAL_THRESHOLD:
            status = "critical"
            health_score = 20
            recommendation = "Critical: Severe vegetation loss detected. Immediate intervention required."
            
        else:
            status = "severely_degraded"
            health_score = 5
            recommendation = "Emergency: Extreme vegetation loss. Urgent conservation action needed."
        
        return {
            'status': status,
            'health_score': health_score,
            'ndvi_value': round(ndvi_value, 3),
            'recommendation': recommendation,
            'thresholds': {
                'healthy': self.HEALTHY_THRESHOLD,
                'moderate': self.MODERATE_THRESHOLD,
                'alert': self.ALERT_THRESHOLD,
                'critical': self.CRITICAL_THRESHOLD
            }
        }
    
    def detect_change(self, before_ndvi: float, after_ndvi: float, 
                     time_diff_days: int) -> Dict[str, any]:
        """
        Detect vegetation change between two NDVI measurements
        
        Args:
            before_ndvi: NDVI value from earlier date
            after_ndvi: NDVI value from later date
            time_diff_days: Time difference in days
            
        Returns:
            Change detection analysis
        """
        change = after_ndvi - before_ndvi
        change_rate = change / time_diff_days if time_diff_days > 0 else 0
        
        # Determine change significance
        if abs(change) < 0.05:
            change_type = "stable"
            significance = "low"
        elif abs(change) < 0.15:
            change_type = "gradual_change"
            significance = "moderate"
        else:
            change_type = "rapid_change"
            significance = "high"
        
        # Direction of change
        if change > 0:
            direction = "improvement"
            trend_description = "Vegetation health is improving"
        elif change < 0:
            direction = "degradation"
            trend_description = "Vegetation health is declining"
        else:
            direction = "stable"
            trend_description = "Vegetation health is stable"
        
        # Alert level based on change
        alert_level = "none"
        if change < -0.1 and after_ndvi < self.ALERT_THRESHOLD:
            alert_level = "high"
        elif change < -0.05:
            alert_level = "medium"
        elif change < -0.02:
            alert_level = "low"
        
        return {
            'change_value': round(change, 3),
            'change_rate_per_day': round(change_rate, 6),
            'change_type': change_type,
            'direction': direction,
            'significance': significance,
            'trend_description': trend_description,
            'alert_level': alert_level,
            'time_period_days': time_diff_days,
            'before_analysis': self.analyze_vegetation_health(before_ndvi),
            'after_analysis': self.analyze_vegetation_health(after_ndvi)
        }
    
    def process_time_series(self, time_series_data: List[Dict]) -> Dict[str, any]:
        """
        Process a time series of NDVI measurements
        
        Args:
            time_series_data: List of dicts with 'date' and 'ndvi' keys
            
        Returns:
            Comprehensive time series analysis
        """
        if not time_series_data or len(time_series_data) < 2:
            return {'error': 'Insufficient data for time series analysis'}
        
        # Sort by date
        sorted_data = sorted(time_series_data, key=lambda x: x['date'])
        ndvi_values = [item['ndvi'] for item in sorted_data]
        dates = [item['date'] for item in sorted_data]
        
        # Basic statistics
        mean_ndvi = np.mean(ndvi_values)
        std_ndvi = np.std(ndvi_values)
        min_ndvi = np.min(ndvi_values)
        max_ndvi = np.max(ndvi_values)
        
        # Trend analysis using linear regression
        x = np.arange(len(ndvi_values))
        coefficients = np.polyfit(x, ndvi_values, 1)
        trend_slope = coefficients[0]
        
        # Determine overall trend
        if abs(trend_slope) < 0.001:
            overall_trend = "stable"
        elif trend_slope > 0:
            overall_trend = "improving"
        else:
            overall_trend = "declining"
        
        # Seasonal analysis (if enough data)
        seasonal_patterns = None
        if len(ndvi_values) >= 12:  # At least a year of monthly data
            seasonal_patterns = self._analyze_seasonal_patterns(sorted_data)
        
        # Anomaly detection
        anomalies = self._detect_anomalies(ndvi_values, mean_ndvi, std_ndvi)
        
        # Change points detection
        change_points = self._detect_change_points(ndvi_values)
        
        return {
            'statistics': {
                'mean_ndvi': round(mean_ndvi, 3),
                'std_ndvi': round(std_ndvi, 3),
                'min_ndvi': round(min_ndvi, 3),
                'max_ndvi': round(max_ndvi, 3),
                'data_points': len(ndvi_values),
                'time_span': {
                    'start_date': dates[0],
                    'end_date': dates[-1]
                }
            },
            'trend_analysis': {
                'overall_trend': overall_trend,
                'trend_slope': round(trend_slope, 6),
                'trend_strength': 'strong' if abs(trend_slope) > 0.01 else 'weak'
            },
            'health_assessment': self.analyze_vegetation_health(mean_ndvi),
            'anomalies': anomalies,
            'change_points': change_points,
            'seasonal_patterns': seasonal_patterns,
            'latest_change': self.detect_change(
                ndvi_values[-2], ndvi_values[-1], 
                (datetime.fromisoformat(dates[-1]) - datetime.fromisoformat(dates[-2])).days
            ) if len(ndvi_values) >= 2 else None
        }
    
    def _analyze_seasonal_patterns(self, time_series_data: List[Dict]) -> Dict[str, any]:
        """Analyze seasonal vegetation patterns"""
        monthly_data = {}
        
        for item in time_series_data:
            date = datetime.fromisoformat(item['date'])
            month = date.month
            
            if month not in monthly_data:
                monthly_data[month] = []
            monthly_data[month].append(item['ndvi'])
        
        # Calculate monthly averages
        monthly_averages = {}
        for month, values in monthly_data.items():
            monthly_averages[month] = {
                'mean_ndvi': round(np.mean(values), 3),
                'std_ndvi': round(np.std(values), 3),
                'data_points': len(values)
            }
        
        # Find peak and low seasons
        month_means = {month: data['mean_ndvi'] for month, data in monthly_averages.items()}
        peak_month = max(month_means, key=month_means.get)
        low_month = min(month_means, key=month_means.get)
        
        return {
            'monthly_averages': monthly_averages,
            'peak_vegetation_month': peak_month,
            'lowest_vegetation_month': low_month,
            'seasonal_variation': round(month_means[peak_month] - month_means[low_month], 3)
        }
    
    def _detect_anomalies(self, ndvi_values: List[float], mean_ndvi: float, 
                         std_ndvi: float, threshold: float = 2.0) -> List[Dict]:
        """Detect anomalous NDVI values using statistical methods"""
        anomalies = []
        
        for i, value in enumerate(ndvi_values):
            z_score = abs(value - mean_ndvi) / std_ndvi if std_ndvi > 0 else 0
            
            if z_score > threshold:
                anomaly_type = "high" if value > mean_ndvi else "low"
                anomalies.append({
                    'index': i,
                    'ndvi_value': round(value, 3),
                    'z_score': round(z_score, 2),
                    'anomaly_type': anomaly_type,
                    'severity': 'extreme' if z_score > 3 else 'moderate'
                })
        
        return anomalies
    
    def _detect_change_points(self, ndvi_values: List[float]) -> List[Dict]:
        """Detect significant change points in NDVI time series"""
        change_points = []
        
        if len(ndvi_values) < 3:
            return change_points
        
        # Simple change point detection using moving window
        window_size = min(5, len(ndvi_values) // 3)
        
        for i in range(window_size, len(ndvi_values) - window_size):
            before_mean = np.mean(ndvi_values[i-window_size:i])
            after_mean = np.mean(ndvi_values[i:i+window_size])
            
            change_magnitude = abs(after_mean - before_mean)
            
            if change_magnitude > 0.1:  # Significant change threshold
                change_points.append({
                    'index': i,
                    'change_magnitude': round(change_magnitude, 3),
                    'change_type': 'increase' if after_mean > before_mean else 'decrease',
                    'before_mean': round(before_mean, 3),
                    'after_mean': round(after_mean, 3)
                })
        
        return change_points
    
    def generate_alert_recommendation(self, analysis_result: Dict) -> Dict[str, any]:
        """
        Generate actionable recommendations based on NDVI analysis
        
        Args:
            analysis_result: Result from NDVI analysis
            
        Returns:
            Recommendations and action items
        """
        health_status = analysis_result.get('health_assessment', {}).get('status', 'unknown')
        trend = analysis_result.get('trend_analysis', {}).get('overall_trend', 'stable')
        
        recommendations = []
        priority = 'low'
        action_required = False
        
        # Health-based recommendations
        if health_status == 'critical' or health_status == 'severely_degraded':
            recommendations.append("Immediate field verification required")
            recommendations.append("Implement emergency conservation measures")
            recommendations.append("Contact local forest officials")
            priority = 'critical'
            action_required = True
            
        elif health_status == 'degraded':
            recommendations.append("Schedule field inspection within 7 days")
            recommendations.append("Monitor for encroachment or illegal activities")
            recommendations.append("Consider soil conservation measures")
            priority = 'high'
            action_required = True
            
        elif health_status == 'moderate':
            recommendations.append("Increase monitoring frequency")
            recommendations.append("Check for early signs of degradation")
            priority = 'medium'
        
        # Trend-based recommendations
        if trend == 'declining':
            recommendations.append("Investigate causes of vegetation decline")
            recommendations.append("Implement preventive conservation strategies")
            if priority == 'low':
                priority = 'medium'
        
        # Anomaly-based recommendations
        anomalies = analysis_result.get('anomalies', [])
        if anomalies:
            recommendations.append(f"Investigate {len(anomalies)} anomalous readings")
            if any(a['severity'] == 'extreme' for a in anomalies):
                priority = 'high'
                action_required = True
        
        return {
            'recommendations': recommendations,
            'priority': priority,
            'action_required': action_required,
            'monitoring_frequency': 'weekly' if priority in ['critical', 'high'] else 'monthly',
            'stakeholders_to_notify': [
                'Forest Department' if priority in ['critical', 'high'] else None,
                'Local Community Leaders' if action_required else None,
                'Environmental NGOs' if priority == 'critical' else None
            ]
        }