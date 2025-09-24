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
from datetime import datetime
from fastapi import FastAPI, Request, Header, HTTPException, Query
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from agents import get_agent_orchestrator
from virtual_filesystem import get_context_manager
from user_containers import container_manager
from onboarding import onboarding_flow
from whoop_integration import get_whoop_integration

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# LLM Integration
def get_llm_client():
    """Get LLM client based on available API keys"""
    if OPENAI_API_KEY:
        try:
            from openai import OpenAI
            return OpenAI(api_key=OPENAI_API_KEY), "openai"
        except ImportError:
            pass
    
    if ANTHROPIC_API_KEY:
        try:
            import anthropic
            return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY), "anthropic"
        except ImportError:
            pass
    
    return None, None

def extract_tenant_from_host(host: str) -> str:
    """Extract tenant ID from host header"""
    if host.startswith("tgaraouy."):
        return "tgaraouy"
    elif "." in host and not host.startswith("www."):
        return host.split(".")[0]
    return "default"

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
    """WHOOP v2 webhook receiver with real-time data processing"""
    tenant_id = tenant or get_tenant_from_request(request)
    whoop_integration = get_whoop_integration(tenant_id)
    
    body = await request.body()
    body_str = body.decode('utf-8')
    
    try:
        webhook_data = json.loads(body_str)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    # Verify signature if provided
    if x_whoop_signature:
        if not whoop_integration.verify_webhook_signature(body_str, x_whoop_signature):
            raise HTTPException(status_code=401, detail="Invalid WHOOP signature")
    
    # Verify token if provided
    token_env = os.getenv("WHOOP_WEBHOOK_TOKEN")
    if token_env and token != token_env:
        raise HTTPException(status_code=401, detail="Invalid webhook token")
    
    # Process WHOOP data
    processed_data = whoop_integration.process_webhook_data(webhook_data)
    
    # Save to context manager
    context_manager = get_context_manager(tenant_id)
    context_manager.save_health_data("whoop_realtime", processed_data)
    
    # Process through agents if we have meaningful data
    if processed_data.get("metrics"):
        orchestrator = get_agent_orchestrator(tenant_id)
        agent_results = await orchestrator.process_health_data(processed_data["metrics"])
        
        # Save agent results
        context_manager.save_agent_result("whoop_processing", agent_results)
    
    return {
        "status": "processed",
        "tenant": tenant_id,
        "data_type": processed_data.get("data_type", "unknown"),
        "insights_count": len(processed_data.get("insights", [])),
        "recommendations_count": len(processed_data.get("recommendations", [])),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/webhook/test/{tenant_id}")
async def test_webhook(tenant_id: str, data: dict):
    return {
        "status": "success",
        "message": f"Webhook test successful for tenant {tenant_id}",
        "tenant_id": tenant_id
    }

# Enhanced endpoints with proper tenant routing
def get_tenant_from_request(request: Request) -> str:
    """Extract tenant ID from request"""
    host = request.headers.get("host", "")
    return extract_tenant_from_host(host)

def get_user_container(request: Request) -> Optional[Any]:
    """Get user container from subdomain"""
    tenant_id = get_tenant_from_request(request)
    return container_manager.get_container(tenant_id)

# Comprehensive Onboarding System
@app.get("/onboarding/start")
async def start_onboarding(request: Request, user_id: Optional[str] = Query(None)):
    """Start comprehensive onboarding process"""
    tenant_id = user_id or get_tenant_from_request(request)
    
    # Check if container already exists
    existing_container = container_manager.get_container(tenant_id)
    if existing_container:
        return {
            "status": "container_exists",
            "message": f"Container for {tenant_id} already exists",
            "dashboard_url": existing_container.get_container_info()["dashboard_url"]
        }
    
    return onboarding_flow.start_onboarding(tenant_id)

@app.get("/onboarding/health-goals")
async def get_health_goals_options():
    """Get available health goals for selection"""
    return {
        "health_goals": onboarding_flow.get_health_goals_options(),
        "message": "Select your health goals to personalize your experience"
    }

@app.get("/onboarding/daily-goals")
async def get_daily_goals_options():
    """Get available daily goals for selection"""
    return {
        "daily_goals": onboarding_flow.get_daily_goals_options(),
        "message": "Choose your daily habits for consistency tracking"
    }

@app.get("/onboarding/health-tools")
async def get_health_tools_options():
    """Get available health tools and devices"""
    return {
        "health_tools": onboarding_flow.get_health_tools_options(),
        "message": "Select the health tools and devices you use"
    }

@app.get("/onboarding/service-catalog")
async def get_service_catalog():
    """Get comprehensive service catalog"""
    return {
        "status": "success",
        "service_catalog": onboarding_flow.get_service_catalog()
    }

@app.get("/onboarding/hybrid-templates")
async def get_hybrid_templates():
    """Get hybrid template combinations"""
    return {
        "status": "success",
        "hybrid_templates": onboarding_flow.get_hybrid_templates()
    }

@app.post("/onboarding/service-recommendations")
async def get_service_recommendations(request: Request):
    """Get service recommendations based on goals and tools"""
    data = await request.json()
    health_goals = data.get("health_goals", [])
    health_tools = data.get("health_tools", [])
    
    return {
        "status": "success",
        "recommendations": onboarding_flow.get_service_recommendations(health_goals, health_tools)
    }

@app.get("/onboarding/templates")
async def get_health_templates():
    """Get available health templates"""
    return {
        "templates": onboarding_flow.get_health_templates(),
        "message": "Choose a health template that matches your lifestyle"
    }

@app.post("/onboarding/step")
async def process_onboarding_step(
    request: Request,
    step: str,
    data: Dict[str, Any],
    user_id: Optional[str] = Query(None)
):
    """Process a specific onboarding step"""
    tenant_id = user_id or get_tenant_from_request(request)
    return onboarding_flow.process_onboarding_step(tenant_id, step, data)

@app.post("/onboarding/complete")
async def complete_onboarding(
    request: Request,
    data: Dict[str, Any],
    user_id: Optional[str] = Query(None)
):
    """Complete the onboarding process"""
    tenant_id = user_id or get_tenant_from_request(request)
    return onboarding_flow.complete_onboarding(tenant_id)

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

# Enhanced UI and file system endpoints
@app.get("/api/context/summary")
async def get_context_summary(request: Request):
    """Get context summary for tenant"""
    tenant_id = get_tenant_from_request(request)
    context_manager = get_context_manager(tenant_id)
    return context_manager.get_context_summary()

@app.get("/api/context/files")
async def list_context_files(request: Request, category: Optional[str] = Query(None)):
    """List files in virtual file system"""
    tenant_id = get_tenant_from_request(request)
    context_manager = get_context_manager(tenant_id)
    files = context_manager.vfs.list_files(category)
    return {
        "tenant_id": tenant_id,
        "category": category,
        "files": files,
        "total_files": len(files)
    }

@app.get("/api/context/insights")
async def get_recent_insights(request: Request, limit: int = Query(10)):
    """Get recent insights"""
    tenant_id = get_tenant_from_request(request)
    context_manager = get_context_manager(tenant_id)
    insights = context_manager.get_recent_insights(limit)
    return {
        "tenant_id": tenant_id,
        "insights": insights,
        "count": len(insights)
    }

@app.get("/api/context/recommendations")
async def get_recent_recommendations(request: Request, limit: int = Query(10)):
    """Get recent recommendations"""
    tenant_id = get_tenant_from_request(request)
    context_manager = get_context_manager(tenant_id)
    recommendations = context_manager.get_recent_recommendations(limit)
    return {
        "tenant_id": tenant_id,
        "recommendations": recommendations,
        "count": len(recommendations)
    }

@app.get("/api/context/agent-history")
async def get_agent_history(request: Request, agent_name: Optional[str] = Query(None)):
    """Get agent processing history"""
    tenant_id = get_tenant_from_request(request)
    context_manager = get_context_manager(tenant_id)
    history = context_manager.get_agent_history(agent_name)
    return {
        "tenant_id": tenant_id,
        "agent_name": agent_name,
        "history": history,
        "count": len(history)
    }

@app.post("/api/llm/chat")
async def chat_with_llm(request: Request, message: str, context: Optional[str] = Query(None)):
    """Chat with LLM for health insights"""
    tenant_id = get_tenant_from_request(request)
    
    # Get LLM client
    client, provider = get_llm_client()
    if not client:
        raise HTTPException(status_code=503, detail="LLM service not available")
    
    try:
        if provider == "openai":
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a health AI assistant for {tenant_id}. Provide personalized health insights and recommendations."},
                    {"role": "user", "content": f"Context: {context or 'No specific context'}\n\nMessage: {message}"}
                ],
                max_tokens=500,
                temperature=0.7
            )
            llm_response = response.choices[0].message.content
        else:  # anthropic
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=500,
                system=f"You are a health AI assistant for {tenant_id}. Provide personalized health insights and recommendations.",
                messages=[{"role": "user", "content": f"Context: {context or 'No specific context'}\n\nMessage: {message}"}]
            )
            llm_response = response.content[0].text
        
        # Save conversation to context
        context_manager = get_context_manager(tenant_id)
        context_manager.vfs.write_file("conversations", f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", {
            "message": message,
            "response": llm_response,
            "context": context,
            "provider": provider
        })
        
        return {
            "tenant_id": tenant_id,
            "message": message,
            "response": llm_response,
            "provider": provider,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM call failed: {str(e)}")

# Daily actions and consistency tracking
@app.get("/api/daily-actions")
async def get_daily_actions(request: Request):
    """Get today's personalized health actions based on user container"""
    container = get_user_container(request)
    if not container:
        raise HTTPException(status_code=404, detail="User container not found. Please complete onboarding first.")
    
    tenant_id = container.user_id
    context_manager = get_context_manager(tenant_id)
    
    # Get personalized daily actions from container
    personalized_actions = container.get_daily_actions()
    
    # Get recent insights and recommendations
    recent_insights = context_manager.get_recent_insights(5)
    recent_recommendations = context_manager.get_recent_recommendations(5)
    
    return {
        "tenant_id": tenant_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "container_info": {
            "health_goals": container.health_goals,
            "health_tools": container.health_tools,
            "agents_enabled": container.agents_enabled
        },
        "insights": recent_insights,
        "recommendations": recent_recommendations,
        "actions_today": personalized_actions,
        "total_actions": len(personalized_actions)
    }

@app.post("/api/daily-actions/{action_id}/complete")
async def complete_daily_action(request: Request, action_id: str):
    """Mark a daily action as completed"""
    tenant_id = get_tenant_from_request(request)
    context_manager = get_context_manager(tenant_id)
    
    # Save completed action
    action_data = {
        "action_id": action_id,
        "completed_at": datetime.now().isoformat(),
        "tenant_id": tenant_id
    }
    
    context_manager.vfs.write_file("daily_actions", f"action_{action_id}_{datetime.now().strftime('%Y%m%d')}.json", action_data)
    
    return {
        "status": "completed",
        "action_id": action_id,
        "completed_at": action_data["completed_at"],
        "message": f"Action '{action_id}' marked as completed"
    }

@app.get("/api/consistency/streak")
async def get_consistency_streak(request: Request):
    """Get consistency streak data"""
    tenant_id = get_tenant_from_request(request)
    context_manager = get_context_manager(tenant_id)
    
    # Get daily actions history
    action_files = context_manager.vfs.list_files("daily_actions")
    
    # Calculate streak (simplified)
    current_streak = 0
    max_streak = 0
    total_actions = len(action_files)
    
    return {
        "tenant_id": tenant_id,
        "current_streak": current_streak,
        "max_streak": max_streak,
        "total_actions": total_actions,
        "consistency_score": min(100, (total_actions * 10)),  # Simplified scoring
        "last_updated": datetime.now().isoformat()
    }

# Container management endpoints
@app.get("/api/container/info")
async def get_container_info(request: Request):
    """Get user container information"""
    container = get_user_container(request)
    if not container:
        raise HTTPException(status_code=404, detail="User container not found. Please complete onboarding first.")
    
    return container.get_container_info()

@app.get("/api/container/actions")
async def get_container_actions(request: Request):
    """Get personalized actions for user container"""
    container = get_user_container(request)
    if not container:
        raise HTTPException(status_code=404, detail="User container not found. Please complete onboarding first.")
    
    return {
        "container_id": container.container_id,
        "user_id": container.user_id,
        "personalized_actions": container.get_daily_actions(),
        "templates_available": list(container.templates_loaded.keys()),
        "agents_active": container.agents_enabled
    }

@app.post("/api/container/update-goals")
async def update_container_goals(request: Request, goals_data: Dict[str, Any]):
    """Update user goals and reconfigure container"""
    container = get_user_container(request)
    if not container:
        raise HTTPException(status_code=404, detail="User container not found. Please complete onboarding first.")
    
    result = container.update_goals(goals_data)
    return result

@app.get("/api/container/services")
async def get_container_services(request: Request):
    """Get container service status and configuration"""
    container = get_user_container(request)
    if not container:
        raise HTTPException(status_code=404, detail="User container not found. Please complete onboarding first.")
    
    return container.get_service_status()

@app.put("/api/container/services/configure")
async def configure_container_services(request: Request, service_config: Dict[str, Any]):
    """Configure container services with granular control"""
    container = get_user_container(request)
    if not container:
        raise HTTPException(status_code=404, detail="User container not found. Please complete onboarding first.")
    
    result = container.update_service_configuration(service_config)
    return result

@app.post("/api/container/services/{service_id}/enable")
async def enable_service(request: Request, service_id: str, priority: str = "medium"):
    """Enable a specific service"""
    container = get_user_container(request)
    if not container:
        raise HTTPException(status_code=404, detail="User container not found. Please complete onboarding first.")
    
    result = container.enable_service(service_id, priority)
    return result

@app.post("/api/container/services/{service_id}/disable")
async def disable_service(request: Request, service_id: str):
    """Disable a specific service"""
    container = get_user_container(request)
    if not container:
        raise HTTPException(status_code=404, detail="User container not found. Please complete onboarding first.")
    
    result = container.disable_service(service_id)
    return result

@app.put("/api/container/services/{service_id}/priority")
async def set_service_priority(request: Request, service_id: str, priority: str):
    """Set priority for a specific service"""
    container = get_user_container(request)
    if not container:
        raise HTTPException(status_code=404, detail="User container not found. Please complete onboarding first.")
    
    result = container.set_service_priority(service_id, priority)
    return result

# Tenant-specific dashboard
@app.get("/dashboard")
async def get_dashboard(request: Request, tenant: Optional[str] = Query(None)):
    """Get tenant dashboard"""
    tenant_id = tenant or get_tenant_from_request(request)
    
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
                <button class="btn" onclick="chatWithLLM()">Chat with AI</button>
            </div>
        </div>
        
        <script>
            async function processData() {{
                const response = await fetch('/agents/process', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{}})
                }});
                const result = await response.json();
                alert('Data processed! Check console for details.');
                console.log('Processing result:', result);
            }}
            
            async function getInsights() {{
                const response = await fetch('/api/context/insights');
                const result = await response.json();
                alert(`Retrieved ${{result.count}} insights! Check console for details.`);
                console.log('Insights:', result);
            }}
            
            async function checkAgents() {{
                const response = await fetch('/agents/status');
                const result = await response.json();
                alert(`${{result.total_agents}} agents are operational!`);
                console.log('Agent status:', result);
            }}
            
            async function getContextSummary() {{
                const response = await fetch('/api/context/summary');
                const result = await response.json();
                console.log('Context summary:', result);
                return result;
            }}
            
            async function chatWithLLM() {{
                const message = prompt('Enter your health question:');
                if (message) {{
                    const response = await fetch(`/api/llm/chat?message=${{encodeURIComponent(message)}}`, {{
                        method: 'POST'
                    }});
                    const result = await response.json();
                    alert(`LLM Response: ${{result.response}}`);
                    console.log('LLM chat:', result);
                }}
            }}
            
            // Load context summary on page load
            window.onload = function() {{
                getContextSummary();
            }};
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)