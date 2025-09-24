#!/usr/bin/env python3
"""
Subdomain Middleware for Vibespan.ai
Handles localhost subdomain routing for development.
"""

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import logging

logger = logging.getLogger(__name__)

class SubdomainMiddleware(BaseHTTPMiddleware):
    """Middleware to handle subdomain routing for development"""
    
    def __init__(self, app, development_mode: bool = True):
        super().__init__(app)
        self.development_mode = development_mode
    
    async def dispatch(self, request: Request, call_next):
        """Process request and handle subdomain routing"""
        
        # Get the host header
        host = request.headers.get("host", "")
        
        # Handle localhost subdomains in development
        if self.development_mode and "localhost" in host:
            # Extract subdomain from localhost
            if "." in host:
                subdomain = host.split(".")[0]
                
                # Add tenant info to request state
                request.state.tenant_id = subdomain
                request.state.is_subdomain_request = True
                
                logger.info(f"Development subdomain detected: {subdomain}")
            else:
                request.state.tenant_id = None
                request.state.is_subdomain_request = False
        
        # Handle production subdomains
        elif "." in host and host.endswith("vibespan.ai"):
            subdomain = host.split(".")[0]
            if subdomain not in ["www", "api"]:
                request.state.tenant_id = subdomain
                request.state.is_subdomain_request = True
            else:
                request.state.tenant_id = None
                request.state.is_subdomain_request = False
        else:
            request.state.tenant_id = None
            request.state.is_subdomain_request = False
        
        # Process the request
        response = await call_next(request)
        
        return response

def get_tenant_id_from_request(request: Request) -> str:
    """Extract tenant ID from request state or headers"""
    # First check if middleware already set it
    if hasattr(request.state, 'tenant_id') and request.state.tenant_id:
        return request.state.tenant_id
    
    # Check Host header for subdomain
    host = request.headers.get("host", "")
    
    # Handle localhost subdomains in development
    if "localhost" in host and "." in host:
        subdomain = host.split(".")[0]
        if subdomain != "localhost":
            return subdomain
    
    # Handle production subdomains
    elif "." in host and host.endswith("vibespan.ai"):
        subdomain = host.split(".")[0]
        if subdomain not in ["www", "api"]:
            return subdomain
    
    # For development, default to tgaraouy if no subdomain detected
    if "localhost" in host:
        return "tgaraouy"
    
    raise HTTPException(status_code=400, detail="Unable to determine tenant from subdomain")
