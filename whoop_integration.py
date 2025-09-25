#!/usr/bin/env python3
"""
WHOOP v2 Integration for Vibespan.ai
Real-time health data processing and analysis.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import hashlib
import hmac

logger = logging.getLogger(__name__)

class WhoopIntegration:
    """Handles WHOOP v2 API integration and data processing"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.client_id = os.getenv("WHOOP_CLIENT_ID")
        self.client_secret = os.getenv("WHOOP_CLIENT_SECRET")
        self.webhook_secret = os.getenv("WHOOP_WEBHOOK_SECRET")
        self.base_url = "https://api.prod.whoop.com"
        self.logger = logging.getLogger(f"whoop.{tenant_id}")
    
    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        """Verify WHOOP webhook signature"""
        if not self.webhook_secret:
            return True  # Skip verification if no secret configured
        
        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    def process_webhook_data(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming WHOOP webhook data"""
        self.logger.info(f"Processing WHOOP webhook for tenant {self.tenant_id}")
        
        try:
            # Extract key metrics from webhook
            processed_data = {
                "timestamp": datetime.now().isoformat(),
                "tenant_id": self.tenant_id,
                "source": "whoop_webhook",
                "data_type": webhook_data.get("type", "unknown"),
                "metrics": self._extract_metrics(webhook_data),
                "raw_data": webhook_data
            }
            
            # Add health insights
            processed_data["insights"] = self._generate_insights(processed_data["metrics"])
            
            # Add recommendations
            processed_data["recommendations"] = self._generate_recommendations(processed_data["metrics"])
            
            return processed_data
            
        except Exception as e:
            self.logger.error(f"WHOOP webhook processing failed: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "tenant_id": self.tenant_id
            }
    
    def _extract_metrics(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key health metrics from webhook data"""
        metrics = {}
        
        # Extract recovery data
        if "recovery" in webhook_data:
            recovery = webhook_data["recovery"]
            metrics["recovery_score"] = recovery.get("score", 0)
            metrics["hrv"] = recovery.get("hrv", 0)
            metrics["resting_heart_rate"] = recovery.get("resting_heart_rate", 0)
            metrics["recovery_timestamp"] = recovery.get("timestamp", datetime.now().isoformat())
        
        # Extract sleep data
        if "sleep" in webhook_data:
            sleep = webhook_data["sleep"]
            metrics["sleep_duration"] = sleep.get("duration", 0) / 3600  # Convert to hours
            metrics["sleep_efficiency"] = sleep.get("efficiency", 0)
            metrics["deep_sleep"] = sleep.get("deep_sleep", 0) / 3600
            metrics["rem_sleep"] = sleep.get("rem_sleep", 0) / 3600
            metrics["light_sleep"] = sleep.get("light_sleep", 0) / 3600
            metrics["sleep_timestamp"] = sleep.get("timestamp", datetime.now().isoformat())
        
        # Extract strain data
        if "strain" in webhook_data:
            strain = webhook_data["strain"]
            metrics["strain_score"] = strain.get("score", 0)
            metrics["kilojoule"] = strain.get("kilojoule", 0)
            metrics["strain_timestamp"] = strain.get("timestamp", datetime.now().isoformat())
        
        # Extract workout data
        if "workout" in webhook_data:
            workout = webhook_data["workout"]
            metrics["workout_duration"] = workout.get("duration", 0) / 60  # Convert to minutes
            metrics["workout_strain"] = workout.get("strain", 0)
            metrics["workout_type"] = workout.get("sport", "unknown")
            metrics["workout_timestamp"] = workout.get("timestamp", datetime.now().isoformat())
        
        return metrics
    
    def _generate_insights(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate health insights from metrics"""
        insights = []
        
        # Recovery insights
        if "recovery_score" in metrics:
            recovery_score = metrics["recovery_score"]
            if recovery_score >= 80:
                insights.append({
                    "type": "recovery",
                    "message": "Excellent recovery! You're ready for high-intensity training.",
                    "priority": "high",
                    "action": "Consider a challenging workout today."
                })
            elif recovery_score >= 60:
                insights.append({
                    "type": "recovery",
                    "message": "Good recovery. Moderate intensity training recommended.",
                    "priority": "medium",
                    "action": "Plan a moderate workout or active recovery."
                })
            else:
                insights.append({
                    "type": "recovery",
                    "message": "Low recovery detected. Focus on rest and recovery.",
                    "priority": "high",
                    "action": "Take a rest day or do light activities only."
                })
        
        # Sleep insights
        if "sleep_duration" in metrics:
            sleep_duration = metrics["sleep_duration"]
            if sleep_duration < 7:
                insights.append({
                    "type": "sleep",
                    "message": f"Only {sleep_duration:.1f} hours of sleep. Aim for 7-9 hours.",
                    "priority": "high",
                    "action": "Prioritize sleep hygiene and earlier bedtime."
                })
            elif sleep_duration > 9:
                insights.append({
                    "type": "sleep",
                    "message": f"Long sleep duration ({sleep_duration:.1f}h). Monitor for oversleeping.",
                    "priority": "medium",
                    "action": "Check if this is due to recovery needs or other factors."
                })
        
        # Strain insights
        if "strain_score" in metrics:
            strain_score = metrics["strain_score"]
            if strain_score > 18:
                insights.append({
                    "type": "strain",
                    "message": f"High strain day ({strain_score}). Monitor recovery closely.",
                    "priority": "high",
                    "action": "Ensure adequate rest and nutrition for recovery."
                })
            elif strain_score < 10:
                insights.append({
                    "type": "strain",
                    "message": f"Low strain day ({strain_score}). Consider adding activity.",
                    "priority": "medium",
                    "action": "Add light exercise or active recovery."
                })
        
        return insights
    
    def _generate_recommendations(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations from metrics"""
        recommendations = []
        
        # Recovery-based recommendations
        if "recovery_score" in metrics:
            recovery_score = metrics["recovery_score"]
            if recovery_score < 60:
                recommendations.extend([
                    {
                        "category": "recovery",
                        "title": "Prioritize Sleep",
                        "description": "Aim for 7-9 hours of quality sleep tonight",
                        "priority": "high"
                    },
                    {
                        "category": "recovery",
                        "title": "Hydration Focus",
                        "description": "Drink extra water to support recovery processes",
                        "priority": "medium"
                    },
                    {
                        "category": "recovery",
                        "title": "Light Movement",
                        "description": "Consider gentle stretching or walking",
                        "priority": "low"
                    }
                ])
            else:
                recommendations.extend([
                    {
                        "category": "training",
                        "title": "Optimize Training",
                        "description": "You're recovered and ready for quality training",
                        "priority": "high"
                    },
                    {
                        "category": "nutrition",
                        "title": "Pre-Workout Fuel",
                        "description": "Eat a balanced meal 2-3 hours before training",
                        "priority": "medium"
                    }
                ])
        
        # Sleep-based recommendations
        if "sleep_duration" in metrics:
            sleep_duration = metrics["sleep_duration"]
            if sleep_duration < 7:
                recommendations.append({
                    "category": "sleep",
                    "title": "Sleep Optimization",
                    "description": "Create a consistent bedtime routine and sleep environment",
                    "priority": "high"
                })
        
        # Strain-based recommendations
        if "strain_score" in metrics:
            strain_score = metrics["strain_score"]
            if strain_score > 18:
                recommendations.append({
                    "category": "recovery",
                    "title": "Active Recovery",
                    "description": "Focus on mobility work and light movement",
                    "priority": "high"
                })
        
        return recommendations
    
    def get_daily_summary(self) -> Dict[str, Any]:
        """Generate daily health summary"""
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "tenant_id": self.tenant_id,
            "status": "active",
            "last_updated": datetime.now().isoformat(),
            "data_sources": ["whoop_webhook"],
            "metrics_tracked": [
                "recovery_score",
                "sleep_duration", 
                "strain_score",
                "heart_rate_variability",
                "resting_heart_rate"
            ]
        }
    
    async def get_user_data(self) -> Optional[Dict[str, Any]]:
        """Fetch real user data from WHOOP API"""
        try:
            # This would need OAuth2 flow implementation
            # For now, return None to indicate no real data available
            self.logger.info(f"Attempting to fetch real WHOOP data for tenant {self.tenant_id}")
            
            # TODO: Implement OAuth2 flow to get access token
            # TODO: Make API calls to WHOOP endpoints
            # TODO: Parse and return real data
            
            return None  # No real data available yet
            
        except Exception as e:
            self.logger.error(f"Error fetching WHOOP data: {e}")
            return None

# Global WHOOP integrations for each tenant
_whoop_integrations: Dict[str, WhoopIntegration] = {}

def get_whoop_integration(tenant_id: str) -> WhoopIntegration:
    """Get or create WHOOP integration for tenant"""
    if tenant_id not in _whoop_integrations:
        _whoop_integrations[tenant_id] = WhoopIntegration(tenant_id)
    return _whoop_integrations[tenant_id]
