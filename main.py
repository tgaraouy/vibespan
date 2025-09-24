#!/usr/bin/env python3
"""
Vibespan.ai - Health Agents in a Box
Multi-tenant AI health platform with subdomain-based isolation.
"""

import os
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager

# Import tenant routes
from src.api.tenant_routes import router as tenant_router
from src.api.webhook_routes import router as webhook_router
from src.middleware.subdomain_middleware import SubdomainMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("🚀 Starting Vibespan.ai - Health Agents in a Box")
    yield
    logger.info("👋 Shutting down Vibespan.ai")

app = FastAPI(
    title="Vibespan.ai",
    description="Multi-tenant AI health platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Subdomain middleware for development
app.add_middleware(SubdomainMiddleware, development_mode=True)

# Include tenant routes
app.include_router(tenant_router)
app.include_router(webhook_router)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Main landing page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Vibespan.ai - Health Agents in a Box</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .hero { text-align: center; margin-bottom: 40px; }
            .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
            .feature { padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
            .cta { text-align: center; margin-top: 40px; }
            .btn { background: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="hero">
                <h1>🏥 Vibespan.ai</h1>
                <h2>Health Agents in a Box</h2>
                <p>Personalized AI health agents for your lifelong wellness journey</p>
            </div>
            
            <div class="features">
                <div class="feature">
                    <h3>🤖 AI Agents</h3>
                    <p>Personalized health agents that learn from your data</p>
                </div>
                <div class="feature">
                    <h3>📊 Real-time Data</h3>
                    <p>WHOOP, Apple Health, and CSV integration</p>
                </div>
                <div class="feature">
                    <h3>🔒 Secure & Private</h3>
                    <p>FHIR-compliant, encrypted, tenant-isolated</p>
                </div>
                <div class="feature">
                    <h3>📈 Lifespan Focus</h3>
                    <p>Long-term health optimization and longevity</p>
                </div>
            </div>
            
            <div class="cta">
                <a href="/signup" class="btn">Get Started</a>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "vibespan.ai"}

@app.get("/signup")
async def signup():
    """User signup page"""
    return {"message": "Signup page - Coming soon!"}

@app.get("/login")
async def login():
    """User login page"""
    return {"message": "Login page - Coming soon!"}

# Subdomain routing will be handled by middleware
@app.middleware("http")
async def subdomain_routing(request: Request, call_next):
    """Route requests to tenant-specific handlers based on subdomain"""
    host = request.headers.get("host", "")
    
    # Extract subdomain
    if host.startswith("vibespan.ai"):
        # Main domain - serve landing page
        response = await call_next(request)
        return response
    elif "." in host and host.endswith("vibespan.ai"):
        # Subdomain - extract user_id and route to tenant
        subdomain = host.split(".")[0]
        if subdomain != "www":
            # Add tenant context to request
            request.state.tenant_id = subdomain
            request.state.is_tenant = True
        else:
            request.state.is_tenant = False
    else:
        request.state.is_tenant = False
    
    response = await call_next(request)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
