#!/usr/bin/env python3
"""
Authentication system for Vibespan.ai
GitHub OAuth integration with JWT tokens.
"""

import os
import json
import jwt
import secrets
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from urllib.parse import urlencode, parse_qs
import logging

logger = logging.getLogger(__name__)

class AuthManager:
    """Manages authentication and user sessions"""
    
    def __init__(self):
        self.jwt_secret = os.getenv("JWT_SECRET_KEY", "default-secret-key")
        self.github_client_id = os.getenv("GITHUB_CLIENT_ID")
        self.github_client_secret = os.getenv("GITHUB_CLIENT_SECRET")
        self.base_url = os.getenv("BASE_URL", "https://vibespan.ai")
        
    def generate_state(self) -> str:
        """Generate a random state for OAuth"""
        return secrets.token_urlsafe(32)
    
    def get_github_auth_url(self, state: str) -> str:
        """Generate GitHub OAuth URL"""
        params = {
            "client_id": self.github_client_id,
            "redirect_uri": f"{self.base_url}/auth/callback",
            "scope": "user:email",
            "state": state
        }
        return f"https://github.com/login/oauth/authorize?{urlencode(params)}"
    
    def exchange_code_for_token(self, code: str) -> Optional[str]:
        """Exchange GitHub code for access token"""
        try:
            import requests
            
            data = {
                "client_id": self.github_client_id,
                "client_secret": self.github_client_secret,
                "code": code
            }
            
            response = requests.post(
                "https://github.com/login/oauth/access_token",
                data=data,
                headers={"Accept": "application/json"}
            )
            
            if response.status_code == 200:
                token_data = response.json()
                return token_data.get("access_token")
            
        except Exception as e:
            logger.error(f"Token exchange failed: {e}")
        
        return None
    
    def get_github_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Get GitHub user information"""
        try:
            import requests
            
            headers = {
                "Authorization": f"token {access_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            # Get user info
            user_response = requests.get("https://api.github.com/user", headers=headers)
            if user_response.status_code != 200:
                return None
            
            user_data = user_response.json()
            
            # Get user email
            email_response = requests.get("https://api.github.com/user/emails", headers=headers)
            primary_email = None
            if email_response.status_code == 200:
                emails = email_response.json()
                primary_email = next((email["email"] for email in emails if email["primary"]), None)
            
            return {
                "github_id": user_data["id"],
                "username": user_data["login"],
                "name": user_data.get("name", user_data["login"]),
                "email": primary_email or user_data.get("email"),
                "avatar_url": user_data.get("avatar_url"),
                "profile_url": user_data.get("html_url")
            }
            
        except Exception as e:
            logger.error(f"GitHub user info fetch failed: {e}")
            return None
    
    def create_jwt_token(self, user_data: Dict[str, Any]) -> str:
        """Create JWT token for authenticated user"""
        payload = {
            "user_id": user_data["github_id"],
            "username": user_data["username"],
            "subdomain": user_data["username"],  # Use GitHub username as subdomain
            "email": user_data["email"],
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(days=30)
        }
        
        return jwt.encode(payload, self.jwt_secret, algorithm="HS256")
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return user data"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=["HS256"])
            return {
                "user_id": payload["user_id"],
                "username": payload["username"],
                "subdomain": payload["subdomain"],
                "email": payload["email"]
            }
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token")
            return None
    
    def create_user_session(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create user session with JWT token"""
        token = self.create_jwt_token(user_data)
        
        return {
            "token": token,
            "user": {
                "id": user_data["github_id"],
                "username": user_data["username"],
                "name": user_data["name"],
                "email": user_data["email"],
                "avatar_url": user_data["avatar_url"],
                "subdomain": user_data["username"]
            },
            "expires_at": (datetime.utcnow() + timedelta(days=30)).isoformat(),
            "dashboard_url": f"https://{user_data['username']}.vibespan.ai/dashboard"
        }

# Global auth manager
auth_manager = AuthManager()
