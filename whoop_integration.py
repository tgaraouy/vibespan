#!/usr/bin/env python3
"""
WHOOP v2 Integration for Vibespan.ai
Real-time health data processing and analysis.
"""

import os
import json
import logging
import aiohttp
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import hashlib
import hmac
import base64

logger = logging.getLogger(__name__)

class WhoopIntegration:
    """Handles WHOOP v2 API integration and data processing"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.client_id = os.getenv("WHOOP_CLIENT_ID")
        self.client_secret = os.getenv("WHOOP_CLIENT_SECRET")
        self.webhook_secret = os.getenv("WHOOP_WEBHOOK_SECRET")
        self.base_url = "https://api.prod.whoop.com"
        self.auth_url = "https://api.prod.whoop.com/oauth/oauth2/auth"
        self.token_url = "https://api.prod.whoop.com/oauth/oauth2/token"
        self.logger = logging.getLogger(f"whoop.{tenant_id}")
        
        # OAuth2 scopes for your profile
        self.scopes = [
            "read:recovery",
            "read:cycles", 
            "read:sleep",
            "read:workout",
            "read:profile",
            "read:body_measurement"
        ]
        
        # User email for authentication
        self.user_email = "tawfik.garaouy@gmail.com"
    
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
            self.logger.info(f"Attempting to fetch real WHOOP data for tenant {self.tenant_id}")
            
            # Get access token
            access_token = await self._get_access_token()
            if not access_token:
                self.logger.error("Failed to get access token")
                return None
            
            # Fetch data from WHOOP API
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                }
                
                # Get current date for data requests
                today = datetime.now().strftime("%Y-%m-%d")
                
                # Fetch recovery data
                recovery_data = await self._fetch_recovery_data(session, headers, today)
                
                # Fetch sleep data
                sleep_data = await self._fetch_sleep_data(session, headers, today)
                
                # Fetch cycle data (strain)
                cycle_data = await self._fetch_cycle_data(session, headers, today)
                
                # Fetch profile data
                profile_data = await self._fetch_profile_data(session, headers)
                
                # Combine all data
                combined_data = {
                    "metrics": {
                        "hrv": recovery_data.get("hrv", 0),
                        "recovery": recovery_data.get("recovery_percentage", 0),
                        "sleep_score": sleep_data.get("sleep_score", 0),
                        "strain": cycle_data.get("strain", 0),
                        "resting_hr": recovery_data.get("resting_heart_rate", 0),
                        "max_hr": profile_data.get("max_heart_rate", 0),
                        "calories_burned": cycle_data.get("calories", 0),
                        "steps": cycle_data.get("steps", 0),
                        "active_time": cycle_data.get("active_time", 0)
                    },
                    "recent_workouts": await self._fetch_workout_data(session, headers),
                    "sleep_data": {
                        "last_night": sleep_data
                    },
                    "profile": profile_data,
                    "data_source": "whoop_api_real",
                    "last_sync": datetime.now().isoformat(),
                    "user_email": self.user_email
                }
                
                self.logger.info(f"Successfully fetched real WHOOP data for {self.user_email}")
                return combined_data
                
        except Exception as e:
            self.logger.error(f"Error fetching WHOOP data: {e}")
            return None
    
    async def _get_access_token(self) -> Optional[str]:
        """Get OAuth2 access token for WHOOP API"""
        try:
            # Check if we have a stored token
            stored_token = await self._get_stored_token()
            if stored_token and not self._is_token_expired(stored_token):
                return stored_token["access_token"]
            
            # If no valid token, we need to start OAuth2 flow
            self.logger.info("No valid token found - OAuth2 flow required")
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting access token: {e}")
            return None
    
    async def _get_stored_token(self) -> Optional[Dict[str, Any]]:
        """Get stored access token from file system"""
        try:
            # Check memory cache first
            if hasattr(self, '_cached_token') and self._cached_token:
                if not self._is_token_expired(self._cached_token):
                    return self._cached_token
                else:
                    # Token expired, clear it
                    self._cached_token = None
            
            # Try to load from file
            token_file = f"tokens/{self.tenant_id}_whoop_token.json"
            if os.path.exists(token_file):
                with open(token_file, 'r') as f:
                    token_data = json.load(f)
                    if not self._is_token_expired(token_data):
                        # Cache it in memory
                        self._cached_token = token_data
                        return token_data
                    else:
                        # Token expired, remove file
                        os.remove(token_file)
            
            return None
        except Exception as e:
            self.logger.error(f"Error getting stored token: {e}")
            return None
    
    def _is_token_expired(self, token: Dict[str, Any]) -> bool:
        """Check if token is expired"""
        try:
            expires_at = token.get("expires_at", 0)
            return datetime.now().timestamp() >= expires_at
        except Exception:
            return True
    
    def get_authorization_url(self) -> str:
        """Get WHOOP OAuth2 authorization URL"""
        try:
            import urllib.parse
            
            base_url = os.getenv('BASE_URL', 'https://vibespan.ai')
            redirect_uri = f"{base_url}/auth/whoop/callback"
            
            params = {
                "response_type": "code",
                "client_id": self.client_id,
                "redirect_uri": redirect_uri,
                "scope": " ".join(self.scopes),
                "state": f"tenant_{self.tenant_id}"
            }
            
            # Log the redirect URI for debugging
            self.logger.info(f"WHOOP OAuth2 redirect URI: {redirect_uri}")
            self.logger.info(f"WHOOP OAuth2 client ID: {self.client_id}")
            
            query_string = urllib.parse.urlencode(params)
            auth_url = f"{self.auth_url}?{query_string}"
            
            self.logger.info(f"WHOOP OAuth2 authorization URL: {auth_url}")
            return auth_url
            
        except Exception as e:
            self.logger.error(f"Error generating authorization URL: {e}")
            return ""
    
    async def exchange_code_for_token(self, code: str) -> Optional[Dict[str, Any]]:
        """Exchange authorization code for access token"""
        try:
            # Prepare token request - WHOOP uses client_secret_post method
            token_data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": f"{os.getenv('BASE_URL', 'https://vibespan.ai')}/auth/whoop/callback",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            
            # Log the request details for debugging
            self.logger.info(f"Token exchange request - URL: {self.token_url}")
            self.logger.info(f"Token exchange request - Data: {token_data}")
            self.logger.info(f"Token exchange request - Client ID: {self.client_id}")
            
            # WHOOP uses client_secret_post method - no Authorization header needed
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            self.logger.info(f"Token exchange request - Headers: {headers}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.token_url,
                    data=token_data,
                    headers=headers
                ) as response:
                    self.logger.info(f"Token exchange response - Status: {response.status}")
                    
                    if response.status == 200:
                        token_response = await response.json()
                        self.logger.info(f"Token exchange response - Success: {token_response}")
                        
                        # Calculate expiration time
                        expires_in = token_response.get("expires_in", 3600)
                        expires_at = datetime.now().timestamp() + expires_in
                        token_response["expires_at"] = expires_at
                        token_response["user_email"] = self.user_email
                        
                        # Store token (in real implementation, store securely)
                        await self._store_token(token_response)
                        
                        self.logger.info(f"Successfully obtained access token for {self.user_email}")
                        return token_response
                    else:
                        error_text = await response.text()
                        self.logger.error(f"Token exchange failed: {response.status} - {error_text}")
                        print(f"WHOOP Token Exchange Error: {response.status} - {error_text}")
                        return None
                        
        except Exception as e:
            self.logger.error(f"Error exchanging code for token: {e}")
            print(f"WHOOP Token Exchange Exception: {e}")
            return None
    
    async def _store_token(self, token: Dict[str, Any]) -> None:
        """Store access token securely"""
        try:
            # Store token in memory for this session
            self._cached_token = token
            
            # Store token in file for persistence
            os.makedirs("tokens", exist_ok=True)
            token_file = f"tokens/{self.tenant_id}_whoop_token.json"
            with open(token_file, 'w') as f:
                json.dump(token, f, indent=2)
            
            self.logger.info(f"Token stored for {self.user_email}")
        except Exception as e:
            self.logger.error(f"Error storing token: {e}")
    
    def set_access_token(self, access_token: str, expires_in: int = 3600) -> None:
        """Manually set access token for testing"""
        try:
            expires_at = datetime.now().timestamp() + expires_in
            self._cached_token = {
                "access_token": access_token,
                "expires_in": expires_in,
                "expires_at": expires_at,
                "user_email": self.user_email
            }
            self.logger.info(f"Access token manually set for {self.user_email}")
        except Exception as e:
            self.logger.error(f"Error setting access token: {e}")
    
    def has_valid_token(self) -> bool:
        """Check if we have a valid access token"""
        try:
            if hasattr(self, '_cached_token') and self._cached_token:
                return not self._is_token_expired(self._cached_token)
            return False
        except Exception as e:
            self.logger.error(f"Error checking token validity: {e}")
            return False
    
    async def refresh_token_if_needed(self) -> bool:
        """Refresh token if it's close to expiration (within 5 minutes)"""
        try:
            stored_token = await self._get_stored_token()
            if not stored_token:
                return False
            
            # Check if token expires within 5 minutes
            expires_at = stored_token.get("expires_at", 0)
            current_time = datetime.now().timestamp()
            time_until_expiry = expires_at - current_time
            
            if time_until_expiry < 300:  # 5 minutes
                self.logger.info(f"Token expires in {time_until_expiry:.0f} seconds, refreshing...")
                # For now, we'll just clear the expired token
                # In a real implementation, we'd use a refresh token
                await self._clear_token()
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Error refreshing token: {e}")
            return False
    
    async def _clear_token(self) -> None:
        """Clear stored token"""
        try:
            # Clear memory cache
            if hasattr(self, '_cached_token'):
                self._cached_token = None
            
            # Remove token file
            token_file = f"tokens/{self.tenant_id}_whoop_token.json"
            if os.path.exists(token_file):
                os.remove(token_file)
            
            self.logger.info(f"Token cleared for {self.tenant_id}")
        except Exception as e:
            self.logger.error(f"Error clearing token: {e}")
    
    async def _fetch_recovery_data(self, session: aiohttp.ClientSession, headers: Dict, date: str) -> Dict[str, Any]:
        """Fetch recovery data from WHOOP API"""
        try:
            # Real WHOOP API call for recovery data
            url = f"{self.base_url}/v1/recovery/date/{date}"
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "hrv": data.get("hrv", 0),
                        "recovery_percentage": data.get("recovery_percentage", 0),
                        "resting_heart_rate": data.get("resting_heart_rate", 0)
                    }
                else:
                        self.logger.warning(f"Recovery API returned {response.status}")
                        return {}
        except Exception as e:
            self.logger.error(f"Error fetching recovery data: {e}")
                return {}
    
    async def _fetch_sleep_data(self, session: aiohttp.ClientSession, headers: Dict, date: str) -> Dict[str, Any]:
        """Fetch sleep data from WHOOP API"""
        try:
            # Real WHOOP API call for sleep data
            url = f"{self.base_url}/v1/sleep/date/{date}"
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "sleep_score": data.get("sleep_score", 0),
                        "duration": data.get("duration", 0),
                        "efficiency": data.get("efficiency", 0),
                        "deep_sleep": data.get("deep_sleep", 0),
                        "rem_sleep": data.get("rem_sleep", 0),
                        "light_sleep": data.get("light_sleep", 0)
                    }
                else:
                        self.logger.warning(f"Sleep API returned {response.status}")
                        return {}
        except Exception as e:
            self.logger.error(f"Error fetching sleep data: {e}")
                return {}
    
    async def _fetch_cycle_data(self, session: aiohttp.ClientSession, headers: Dict, date: str) -> Dict[str, Any]:
        """Fetch cycle data (strain) from WHOOP API"""
        try:
                url = f"{self.base_url}/v1/cycle/date/{date}"
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "strain": data.get("strain", 0),
                            "calories": data.get("calories", 0),
                            "steps": data.get("steps", 0),
                            "active_time": data.get("active_time", 0)
                        }
                    else:
                        self.logger.warning(f"Cycle API returned {response.status}")
                        return {}
        except Exception as e:
            self.logger.error(f"Error fetching cycle data: {e}")
                return {}
    
    async def _fetch_profile_data(self, session: aiohttp.ClientSession, headers: Dict) -> Dict[str, Any]:
        """Fetch profile data from WHOOP API"""
        try:
                url = f"{self.base_url}/v1/user/profile"
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "email": self.user_email,
                            "max_heart_rate": data.get("max_heart_rate", 0),
                            "height": data.get("height", 0),
                            "weight": data.get("weight", 0)
                        }
                    else:
                        self.logger.warning(f"Profile API returned {response.status}")
                        return {"email": self.user_email}
        except Exception as e:
            self.logger.error(f"Error fetching profile data: {e}")
            return {}
    
    async def _fetch_workout_data(self, session: aiohttp.ClientSession, headers: Dict) -> List[Dict[str, Any]]:
        """Fetch workout data from WHOOP API"""
        try:
                url = f"{self.base_url}/v1/workout"
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        workouts = data.get("workouts", []) if isinstance(data, dict) else data
                        result: List[Dict[str, Any]] = []
                        for w in workouts:
                            result.append({
                                "date": (w.get("start_time") or "").split("T")[0],
                                "type": w.get("activity_type") or w.get("sport") or "Unknown",
                                "duration": round((w.get("duration") or 0) / 60, 0),
                                "strain": w.get("strain", 0),
                                "calories": w.get("calories", 0)
                            })
                        return result
                    else:
                        self.logger.warning(f"Workout API returned {response.status}")
                        return []
        except Exception as e:
            self.logger.error(f"Error fetching workout data: {e}")
            return []

# Global WHOOP integrations for each tenant
_whoop_integrations: Dict[str, WhoopIntegration] = {}

def get_whoop_integration(tenant_id: str) -> WhoopIntegration:
    """Get or create WHOOP integration for tenant"""
    if tenant_id not in _whoop_integrations:
        _whoop_integrations[tenant_id] = WhoopIntegration(tenant_id)
    return _whoop_integrations[tenant_id]
