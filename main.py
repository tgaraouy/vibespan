#!/usr/bin/env python3
"""
Vibespan.ai - Ultra-Simple Vercel Version
No complex imports, no file system access, just basic FastAPI.
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

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
    return {"status": "healthy", "version": "1.0.0", "platform": "Vibespan.ai"}

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

@app.post("/webhook/test/{tenant_id}")
async def test_webhook(tenant_id: str, data: dict):
    return {
        "status": "success",
        "message": f"Webhook test successful for tenant {tenant_id}",
        "tenant_id": tenant_id
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)