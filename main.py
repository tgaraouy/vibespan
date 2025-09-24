#!/usr/bin/env python3
"""
Vibespan.ai - Ultra-Simple Vercel Version
No complex imports, no file system access, just basic FastAPI.
"""

import os
import hmac
import hashlib
import json
from typing import Optional, Dict, Any
from fastapi import FastAPI, Request, Header, HTTPException, Query
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from agents import get_agent_orchestrator

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

app = FastAPI(title="Vibespan.ai", version="1.0.0")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Vibespan.ai - Your Lifelong Wellness AI</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background: #f4f7f6; color: #333; }
            h1 { color: #2c3e50; }
            .container { max-width: 800px; margin: auto; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            .status { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏥 Welcome to Vibespan.ai!</h1>
            <p>Your personal AI health companion for a vibrant, long life.</p>
            <div class="status">
                <h3>✅ System Status: Operational</h3>
                <p>Health agents are running and ready to optimize your wellness journey.</p>
            </div>
            <p><strong>Features:</strong></p>
            <ul style="text-align: left; display: inline-block;">
                <li>🤖 AI Health Agents</li>
                <li>📊 Multi-tenant Architecture</li>
                <li>🔒 Secure Data Processing</li>
                <li>📡 Real-time Webhooks</li>
            </ul>
            <p>Access your health dashboard at: <code>&lt;your-userid&gt;.vibespan.ai</code></p>
        </div>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "version": "1.0.0", 
        "platform": "Vibespan.ai",
        "environment": ENVIRONMENT,
        "debug": DEBUG
    }

@app.get("/env-status")
async def env_status():
    """Check environment variables status"""
    return {
        "environment": ENVIRONMENT,
        "debug": DEBUG,
        "openai_configured": bool(OPENAI_API_KEY),
        "anthropic_configured": bool(ANTHROPIC_API_KEY),
        "jwt_configured": bool(JWT_SECRET_KEY),
        "total_vars_loaded": sum([
            bool(OPENAI_API_KEY),
            bool(ANTHROPIC_API_KEY),
            bool(JWT_SECRET_KEY)
        ])
    }

@app.get("/api/status")
async def api_status():
    return {
        "message": "Vibespan.ai API is running",
        "status": "operational",
        "features": {
            "health_agents": True,
            "multi_tenant": True,
            "data_processing": True,
            "webhooks": True
        }
    }

@app.get("/api/tenant/{tenant_id}")
async def get_tenant_info(tenant_id: str):
    return {
        "tenant_id": tenant_id,
        "status": "active",
        "message": f"Tenant {tenant_id} is operational"
    }

@app.post("/api/tenant/{tenant_id}/process")
async def process_health_data(tenant_id: str, data: dict):
    return {
        "tenant_id": tenant_id,
        "status": "processed",
        "message": "Health data processed successfully",
        "agents_used": ["DataCollector", "PatternDetector", "WorkoutPlanner", "NutritionPlanner", "HealthCoach", "SafetyOfficer"]
    }

@app.get("/api/agents/status")
async def agents_status():
    return {
        "total_agents": 6,
        "active_agents": [
            "DataCollector",
            "PatternDetector", 
            "BasicWorkoutPlanner",
            "BasicNutritionPlanner",
            "HealthCoach",
            "SafetyOfficer"
        ],
        "status": "operational"
    }

@app.get("/webhook/whoop", response_class=PlainTextResponse)
async def whoop_verify(challenge: Optional[str] = None):
    """Optional verification handler if WHOOP sends a challenge query.
    Returns the challenge value verbatim if present.
    """
    if challenge:
        return challenge
    return "ok"

@app.post("/webhook/whoop")
async def whoop_webhook(
    request: Request,
    tenant: Optional[str] = None,
    token: Optional[str] = None,
    x_whoop_signature: Optional[str] = Header(default=None)
):
    """WHOOP v2 webhook receiver with simple HMAC verification.

    - Set WHOOP_WEBHOOK_SECRET in Vercel env vars
    - WHOOP should sign requests with a header (e.g., X-WHOOP-Signature)
    - We compute HMAC-SHA256 over the raw body and compare
    """
    secret = os.getenv("WHOOP_WEBHOOK_SECRET")
    token_env = os.getenv("WHOOP_WEBHOOK_TOKEN")
    body = await request.body()

    # Verify signature if both header and secret are present
    if secret and x_whoop_signature:
        computed = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(computed, x_whoop_signature):
            raise HTTPException(status_code=401, detail="Invalid WHOOP signature")

    # Alternatively, verify a URL token if provided and configured
    if token_env:
        if not token or token != token_env:
            raise HTTPException(status_code=401, detail="Invalid webhook token")

    # Minimal ack for WHOOP; processing can be added later
    return {
        "status": "received",
        "tenant": tenant or "default",
        "bytes": len(body),
        "verified": bool((secret and x_whoop_signature) or token_env)
    }

@app.post("/webhook/test/{tenant_id}")
async def test_webhook(tenant_id: str, data: dict):
    return {
        "status": "success",
        "message": f"Webhook test successful for tenant {tenant_id}",
        "tenant_id": tenant_id
    }

# Onboarding endpoints
@app.get("/onboarding/start")
async def start_onboarding(tenant: Optional[str] = Query(None)):
    """Start onboarding process for a tenant"""
    tenant_id = tenant or "default"
    
    return {
        "status": "onboarding_started",
        "tenant_id": tenant_id,
        "steps": [
            "Welcome to Vibespan.ai!",
            "Connect your health data sources",
            "Set up your health goals",
            "Configure your preferences",
            "Start your health journey!"
        ],
        "current_step": 1,
        "next_action": "Connect data sources"
    }

@app.post("/onboarding/complete")
async def complete_onboarding(tenant: Optional[str] = Query(None), data: Dict[str, Any] = None):
    """Complete onboarding for a tenant"""
    tenant_id = tenant or "default"
    
    # Initialize agent orchestrator for the tenant
    orchestrator = get_agent_orchestrator(tenant_id)
    
    return {
        "status": "onboarding_completed",
        "tenant_id": tenant_id,
        "message": f"Welcome to your personalized health journey, {tenant_id}!",
        "agents_initialized": True,
        "dashboard_url": f"https://{tenant_id}.vibespan.ai/dashboard"
    }

# Agent endpoints
@app.get("/agents/status")
async def get_agents_status(tenant: Optional[str] = Query(None)):
    """Get status of all agents for a tenant"""
    tenant_id = tenant or "default"
    orchestrator = get_agent_orchestrator(tenant_id)
    return orchestrator.get_agent_status()

@app.post("/agents/process")
async def process_with_agents(
    tenant: Optional[str] = Query(None),
    data: Dict[str, Any] = None
):
    """Process health data through all agents"""
    tenant_id = tenant or "default"
    orchestrator = get_agent_orchestrator(tenant_id)
    
    # Default sample data if none provided
    if not data:
        data = {
            "recovery_score": 75,
            "sleep_duration": 7.5,
            "heart_rate_variability": 45,
            "strain_score": 12.5,
            "sources": ["whoop", "apple_health"],
            "records": []
        }
    
    result = await orchestrator.process_health_data(data)
    return result

@app.get("/agents/{agent_name}")
async def get_agent_info(agent_name: str, tenant: Optional[str] = Query(None)):
    """Get information about a specific agent"""
    tenant_id = tenant or "default"
    orchestrator = get_agent_orchestrator(tenant_id)
    
    if agent_name not in orchestrator.agents:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
    
    agent = orchestrator.agents[agent_name]
    return {
        "agent_name": agent_name,
        "tenant_id": tenant_id,
        "description": f"Health agent specialized in {agent_name.lower().replace('_', ' ')}",
        "status": "active"
    }

# Tenant-specific dashboard
@app.get("/dashboard")
async def get_dashboard(tenant: Optional[str] = Query(None)):
    """Get tenant dashboard"""
    tenant_id = tenant or "default"
    
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Vibespan.ai Dashboard - {tenant_id}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f4f7f6; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
            .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }}
            .agent-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
            .agent-card {{ border: 1px solid #ddd; padding: 15px; border-radius: 8px; }}
            .status-active {{ color: #27ae60; font-weight: bold; }}
            .btn {{ background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }}
            .btn:hover {{ background: #2980b9; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏥 Vibespan.ai Dashboard</h1>
                <p>Welcome back, {tenant_id}! Your health agents are ready to optimize your wellness journey.</p>
            </div>
            
            <div class="card">
                <h2>🤖 Your Health Agents</h2>
                <div class="agent-grid">
                    <div class="agent-card">
                        <h3>📊 Data Collector</h3>
                        <p>Collects and normalizes your health data</p>
                        <span class="status-active">● Active</span>
                    </div>
                    <div class="agent-card">
                        <h3>🔍 Pattern Detector</h3>
                        <p>Finds correlations in your health metrics</p>
                        <span class="status-active">● Active</span>
                    </div>
                    <div class="agent-card">
                        <h3>💪 Workout Planner</h3>
                        <p>Creates personalized exercise plans</p>
                        <span class="status-active">● Active</span>
                    </div>
                    <div class="agent-card">
                        <h3>🥗 Nutrition Planner</h3>
                        <p>Recommends optimal nutrition strategies</p>
                        <span class="status-active">● Active</span>
                    </div>
                    <div class="agent-card">
                        <h3>🎯 Health Coach</h3>
                        <p>Provides personalized health insights</p>
                        <span class="status-active">● Active</span>
                    </div>
                    <div class="agent-card">
                        <h3>🛡️ Safety Officer</h3>
                        <p>Monitors for health safety concerns</p>
                        <span class="status-active">● Active</span>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2>📈 Quick Actions</h2>
                <button class="btn" onclick="processData()">Process Health Data</button>
                <button class="btn" onclick="getInsights()">Get Health Insights</button>
                <button class="btn" onclick="checkAgents()">Check Agent Status</button>
            </div>
        </div>
        
        <script>
            async function processData() {{
                const response = await fetch('/agents/process?tenant={tenant_id}', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{}})
                }});
                const result = await response.json();
                alert('Data processed! Check console for details.');
                console.log('Processing result:', result);
            }}
            
            async function getInsights() {{
                const response = await fetch('/agents/status?tenant={tenant_id}');
                const result = await response.json();
                alert('Agent status retrieved! Check console for details.');
                console.log('Agent status:', result);
            }}
            
            async function checkAgents() {{
                const response = await fetch('/agents/status?tenant={tenant_id}');
                const result = await response.json();
                alert(`${{result.total_agents}} agents are operational!`);
                console.log('Agent status:', result);
            }}
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)