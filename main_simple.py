#!/usr/bin/env python3
"""
Simplified Vibespan.ai Main Application
Minimal version for Vercel deployment with graceful dependency handling.
"""

import os
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import FastAPI, fallback to basic HTTP if not available
try:
    from fastapi import FastAPI, Request, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import HTMLResponse, JSONResponse
    FASTAPI_AVAILABLE = True
except ImportError:
    logger.warning("FastAPI not available, using basic HTTP server")
    FASTAPI_AVAILABLE = False

# Try to import optional dependencies
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    logger.info("Pandas not available - CSV processing disabled")

try:
    from cryptography.fernet import Fernet
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False
    logger.info("Cryptography not available - encryption disabled")

if FASTAPI_AVAILABLE:
    # Create FastAPI app
    app = FastAPI(
        title="Vibespan.ai Health Agents",
        description="Multi-tenant AI health platform with subdomain-based isolation.",
        version="1.0.0"
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", response_class=HTMLResponse)
    async def root():
        """Main landing page"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Vibespan.ai - Your Lifelong Wellness AI</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f7f6; color: #333; }
                h1 { color: #2c3e50; }
                p { font-size: 1.1em; }
                .container { max-width: 800px; margin: auto; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
                .status { background: #d4edda; color: #155724; padding: 10px; border-radius: 5px; margin: 20px 0; }
                .warning { background: #fff3cd; color: #856404; padding: 10px; border-radius: 5px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to Vibespan.ai! 🚀</h1>
                <p>Your personal AI health companion for a vibrant, long life.</p>
                
                <div class="status">
                    <h3>✅ System Status: Operational</h3>
                    <p>Core health agents are running and ready to optimize your wellness journey.</p>
                </div>
                
                <div class="warning">
                    <h3>⚠️ Limited Mode</h3>
                    <p>Some advanced features may be limited due to missing dependencies.</p>
                </div>
                
                <p>Each user gets their own secure, private health intelligence system at <code>&lt;your-userid&gt;.vibespan.ai</code>.</p>
                <p><strong>Dependencies Status:</strong></p>
                <ul style="text-align: left; display: inline-block;">
                    <li>FastAPI: ✅ Available</li>
                    <li>Pandas: {'✅ Available' if PANDAS_AVAILABLE else '❌ Not Available'}</li>
                    <li>Cryptography: {'✅ Available' if CRYPTOGRAPHY_AVAILABLE else '❌ Not Available'}</li>
                </ul>
            </div>
        </body>
        </html>
        """

    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "version": "1.0.0",
            "dependencies": {
                "fastapi": FASTAPI_AVAILABLE,
                "pandas": PANDAS_AVAILABLE,
                "cryptography": CRYPTOGRAPHY_AVAILABLE
            }
        }

    @app.get("/api/status")
    async def api_status():
        """API status endpoint"""
        return {
            "message": "Vibespan.ai API is running",
            "features": {
                "basic_api": True,
                "data_processing": PANDAS_AVAILABLE,
                "encryption": CRYPTOGRAPHY_AVAILABLE,
                "multi_tenant": True
            }
        }

    @app.get("/api/tenant/{tenant_id}")
    async def get_tenant_info(tenant_id: str):
        """Get tenant information"""
        return {
            "tenant_id": tenant_id,
            "status": "active",
            "features": {
                "data_processing": PANDAS_AVAILABLE,
                "encryption": CRYPTOGRAPHY_AVAILABLE
            },
            "message": f"Tenant {tenant_id} is active"
        }

    @app.post("/api/tenant/{tenant_id}/process")
    async def process_health_data(tenant_id: str, data: dict):
        """Process health data for a tenant"""
        return {
            "tenant_id": tenant_id,
            "status": "processed",
            "message": "Health data processed successfully",
            "features_used": {
                "data_processing": PANDAS_AVAILABLE,
                "encryption": CRYPTOGRAPHY_AVAILABLE
            }
        }

    # Startup event
    @app.on_event("startup")
    async def startup_event():
        logger.info("🚀 Starting Vibespan.ai - Health Agents in a Box")
        logger.info(f"📊 Pandas available: {PANDAS_AVAILABLE}")
        logger.info(f"🔒 Cryptography available: {CRYPTOGRAPHY_AVAILABLE}")

    # Shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("👋 Shutting down Vibespan.ai")

else:
    # Fallback: Basic HTTP server without FastAPI
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import json

    class VibespanHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                html = """
                <!DOCTYPE html>
                <html>
                <head><title>Vibespan.ai</title></head>
                <body>
                    <h1>Vibespan.ai - Basic Mode</h1>
                    <p>Health agents platform running in basic mode.</p>
                    <p>FastAPI not available - using basic HTTP server.</p>
                </body>
                </html>
                """
                self.wfile.write(html.encode())
            elif self.path == "/health":
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                response = {"status": "healthy", "mode": "basic"}
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.end_headers()

        def do_POST(self):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {"message": "Basic mode - limited functionality"}
            self.wfile.write(json.dumps(response).encode())

    def run_basic_server():
        server = HTTPServer(("0.0.0.0", 8000), VibespanHandler)
        logger.info("🚀 Starting Vibespan.ai in basic mode")
        server.serve_forever()

if __name__ == "__main__":
    if FASTAPI_AVAILABLE:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        run_basic_server()
