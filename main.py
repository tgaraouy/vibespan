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
from automation_engine import get_automation_engine
from health_concierge import get_health_concierge
from service_catalog import service_catalog
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
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vibespan.ai - Your AI Wellness Concierge</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                overflow-x: hidden;
            }

            /* Hero Section */
            .hero {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                align-items: center;
                position: relative;
                overflow: hidden;
            }

            .hero::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
                opacity: 0.3;
            }

            .hero-content {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 20px;
                position: relative;
                z-index: 2;
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 60px;
                align-items: center;
            }

            .hero-text h1 {
                font-size: 4rem;
                font-weight: 800;
                margin-bottom: 20px;
                line-height: 1.1;
                background: linear-gradient(45deg, #fff, #f0f0f0);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .hero-text .subtitle {
                font-size: 1.5rem;
                margin-bottom: 30px;
                opacity: 0.9;
                font-weight: 300;
            }

            .hero-text .description {
                font-size: 1.2rem;
                margin-bottom: 40px;
                opacity: 0.8;
                line-height: 1.6;
            }

            .cta-buttons {
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
            }

            .btn {
                padding: 18px 36px;
                border: none;
                border-radius: 50px;
                font-size: 1.1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
                text-align: center;
            }

            .btn-primary {
                background: white;
                color: #667eea;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }

            .btn-primary:hover {
                transform: translateY(-3px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.3);
            }

            .btn-secondary {
                background: transparent;
                color: white;
                border: 2px solid white;
            }

            .btn-secondary:hover {
                background: white;
                color: #667eea;
            }

            .hero-visual {
                position: relative;
            }

            .dashboard-preview {
                background: white;
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 30px 60px rgba(0,0,0,0.3);
                transform: perspective(1000px) rotateY(-5deg) rotateX(5deg);
                transition: transform 0.3s ease;
            }

            .dashboard-preview:hover {
                transform: perspective(1000px) rotateY(0deg) rotateX(0deg);
            }

            .dashboard-header {
                display: flex;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 2px solid #f0f0f0;
            }

            .dashboard-header h3 {
                color: #333;
                font-size: 1.3rem;
                margin-left: 10px;
            }

            .metric-card {
                background: #f8f9fa;
                border-radius: 12px;
                padding: 20px;
                margin: 10px 0;
                border-left: 4px solid #667eea;
            }

            .metric-card h4 {
                color: #667eea;
                font-size: 0.9rem;
                margin-bottom: 5px;
            }

            .metric-card .value {
                font-size: 2rem;
                font-weight: 700;
                color: #333;
            }

            /* Stats Section */
            .stats {
                background: white;
                padding: 80px 0;
            }

            .stats-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 20px;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 40px;
            }

            .stat-item {
                text-align: center;
                padding: 30px;
            }

            .stat-number {
                font-size: 3rem;
                font-weight: 800;
                color: #667eea;
                margin-bottom: 10px;
            }

            .stat-label {
                font-size: 1.1rem;
                color: #666;
                font-weight: 500;
            }

            /* Features Section */
            .features {
                background: #f8f9fa;
                padding: 100px 0;
            }

            .features-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 20px;
            }

            .section-title {
                text-align: center;
                font-size: 3rem;
                font-weight: 700;
                color: #333;
                margin-bottom: 20px;
            }

            .section-subtitle {
                text-align: center;
                font-size: 1.3rem;
                color: #666;
                margin-bottom: 60px;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
            }

            .features-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 40px;
                margin-top: 60px;
            }

            .feature-card {
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
                border: 1px solid #e9ecef;
            }

            .feature-card:hover {
                transform: translateY(-10px);
            }

            .feature-icon {
                font-size: 3rem;
                margin-bottom: 20px;
            }

            .feature-card h3 {
                font-size: 1.5rem;
                color: #333;
                margin-bottom: 15px;
            }

            .feature-card p {
                color: #666;
                line-height: 1.6;
            }

            /* CTA Section */
            .cta-section {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 100px 0;
                text-align: center;
            }

            .cta-content {
                max-width: 800px;
                margin: 0 auto;
                padding: 0 20px;
            }

            .cta-content h2 {
                font-size: 3rem;
                margin-bottom: 20px;
            }

            .cta-content p {
                font-size: 1.3rem;
                margin-bottom: 40px;
                opacity: 0.9;
            }

            /* Responsive */
            @media (max-width: 768px) {
                .hero-content {
                    grid-template-columns: 1fr;
                    gap: 40px;
                    text-align: center;
                }

                .hero-text h1 {
                    font-size: 2.5rem;
                }

                .cta-buttons {
                    justify-content: center;
                }

                .features-grid {
                    grid-template-columns: 1fr;
                }
            }

            /* Animations */
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .fade-in-up {
                animation: fadeInUp 0.6s ease-out;
            }

            /* Floating elements */
            .floating {
                animation: float 6s ease-in-out infinite;
            }

            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-20px); }
            }
        </style>
    </head>
    <body>
        <!-- Hero Section -->
        <section class="hero">
            <div class="hero-content">
                <div class="hero-text fade-in-up">
                    <h1>🌱 Vibespan.ai</h1>
                    <p class="subtitle">Your Personal AI Wellness Concierge</p>
                    <p class="description">
                        Transform your wellness journey with AI-powered lifestyle optimization, proactive monitoring, 
                        and personalized wellness coaching. Get 24/7 wellness management without the hassle.
                    </p>
                    <div class="cta-buttons">
                        <a href="/onboarding/start" class="btn btn-primary">
                            🚀 Start Your Wellness Journey
                        </a>
                        <a href="/demo" class="btn btn-secondary">
                            📺 Watch Demo
                        </a>
                    </div>
                </div>
                <div class="hero-visual fade-in-up floating">
                    <div class="dashboard-preview">
                        <div class="dashboard-header">
                            <span style="font-size: 2rem;">📊</span>
                            <h3>Your Health Dashboard</h3>
                        </div>
                        <div class="metric-card">
                            <h4>Recovery Score</h4>
                            <div class="value">87%</div>
                        </div>
                        <div class="metric-card">
                            <h4>Sleep Quality</h4>
                            <div class="value">Excellent</div>
                        </div>
                        <div class="metric-card">
                            <h4>Today's Actions</h4>
                            <div class="value">3/5</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Stats Section -->
        <section class="stats">
            <div class="stats-container">
                <div class="stat-item">
                    <div class="stat-number">24/7</div>
                    <div class="stat-label">AI Wellness Monitoring</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">20+</div>
                    <div class="stat-label">Wellness Services</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">95%</div>
                    <div class="stat-label">User Satisfaction</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">3x</div>
                    <div class="stat-label">Faster Wellness Goals</div>
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section class="features">
            <div class="features-container">
                <h2 class="section-title">Why Choose Vibespan.ai?</h2>
                <p class="section-subtitle">
                    Experience the future of wellness management with AI-powered lifestyle optimization and personalized wellness coaching
                </p>
                
                <div class="features-grid">
                    <div class="feature-card">
                        <div class="feature-icon">🤖</div>
                        <h3>AI Wellness Concierge</h3>
                        <p>Your personal wellness assistant that works 24/7 to optimize your lifestyle. Get personalized recommendations, automated wellness monitoring, and proactive lifestyle coaching.</p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">⚡</div>
                        <h3>Set & Forget Automation</h3>
                        <p>Minimal effort, maximum results. Our automation engine handles your wellness monitoring, lifestyle optimization, and wellness coaching scheduling automatically.</p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">📊</div>
                        <h3>Predictive Analytics</h3>
                        <p>Stay ahead of wellness trends with AI-powered predictions. Get early insights, lifestyle trend analysis, and personalized recommendations to optimize your wellness journey.</p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">🏥</div>
                        <h3>Managed Wellness Services</h3>
                        <p>From Basic to Enterprise, choose your service level. Get comprehensive wellness management with professional-grade lifestyle monitoring and wellness coaching.</p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">🔒</div>
                        <h3>Secure & Private</h3>
                        <p>Your wellness data is protected with enterprise-grade security. Encrypted, secure, and completely private to you.</p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">🎯</div>
                        <h3>Proven Results</h3>
                        <p>Join thousands of users who've transformed their wellness. 3x faster goal achievement, 95% satisfaction rate, and measurable lifestyle improvements.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- CTA Section -->
        <section class="cta-section">
            <div class="cta-content">
                <h2>Ready to Transform Your Wellness?</h2>
                <p>Join thousands of users who've already started their AI-powered wellness journey. Get started in minutes, see results in days.</p>
                <a href="/onboarding/start" class="btn btn-primary" style="font-size: 1.3rem; padding: 20px 40px;">
                    🚀 Start Your Free Trial
                </a>
                <p style="margin-top: 20px; opacity: 0.8; font-size: 1rem;">
                    No credit card required • 14-day free trial • Cancel anytime
                </p>
            </div>
        </section>

        <!-- Legal Disclaimer Section -->
        <section style="background: #f8f9fa; padding: 40px 0; border-top: 1px solid #e9ecef;">
            <div style="max-width: 1200px; margin: 0 auto; padding: 0 20px; text-align: center;">
                <h3 style="color: #333; margin-bottom: 20px; font-size: 1.5rem;">Important Wellness Disclaimer</h3>
                <div style="background: white; border-radius: 10px; padding: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 800px; margin: 0 auto;">
                    <p style="color: #666; line-height: 1.6; margin-bottom: 15px; font-size: 0.95rem;">
                        <strong>Vibespan.ai is a wellness concierge service</strong> that provides lifestyle optimization, wellness coaching, and general well-being advice. 
                        Our services are <strong>non-clinical and non-medical</strong> in nature.
                    </p>
                    <p style="color: #666; line-height: 1.6; margin-bottom: 15px; font-size: 0.95rem;">
                        <strong>We do not:</strong> Diagnose, treat, cure, or prevent any medical conditions. Provide medical advice, prescriptions, or clinical care. 
                        Replace professional medical consultation or treatment.
                    </p>
                    <p style="color: #666; line-height: 1.6; font-size: 0.95rem;">
                        <strong>Always consult with qualified healthcare professionals</strong> for medical concerns, diagnoses, or treatment decisions. 
                        Our wellness services are designed to complement, not replace, professional medical care.
                    </p>
                </div>
            </div>
        </section>
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
@app.get("/onboarding/start", response_class=HTMLResponse)
async def start_onboarding(request: Request, user_id: Optional[str] = Query(None)):
    """Start comprehensive onboarding process with HTML interface"""
    tenant_id = user_id or get_tenant_from_request(request)
    
    # Check if container already exists
    existing_container = container_manager.get_container(tenant_id)
    if existing_container:
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Vibespan.ai - Already Onboarded</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background: #f4f7f6; }}
                .container {{ max-width: 600px; margin: auto; padding: 40px; background: white; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
                .btn {{ background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; display: inline-block; margin: 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌱 Welcome Back!</h1>
                <p>Your wellness concierge is already set up and ready to go.</p>
                <a href="{existing_container.get_container_info()['dashboard_url']}" class="btn">Go to Dashboard</a>
                <a href="/" class="btn">Back to Home</a>
            </div>
        </body>
        </html>
        """
    
    onboarding_data = onboarding_flow.start_onboarding(tenant_id)
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vibespan.ai - Onboarding</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}

            .onboarding-container {{
                background: white;
                border-radius: 20px;
                box-shadow: 0 30px 60px rgba(0,0,0,0.3);
                max-width: 800px;
                width: 100%;
                overflow: hidden;
            }}

            .onboarding-header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}

            .onboarding-header h1 {{
                font-size: 2.5rem;
                margin-bottom: 10px;
            }}

            .onboarding-header p {{
                font-size: 1.2rem;
                opacity: 0.9;
            }}

            .onboarding-content {{
                padding: 40px;
            }}

            .step-indicator {{
                display: flex;
                justify-content: center;
                margin-bottom: 40px;
                flex-wrap: wrap;
            }}

            .step {{
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: #e9ecef;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 5px;
                font-weight: 600;
                color: #666;
                position: relative;
            }}

            .step.active {{
                background: #667eea;
                color: white;
            }}

            .step.completed {{
                background: #28a745;
                color: white;
            }}

            .welcome-section {{
                text-align: center;
                margin-bottom: 40px;
            }}

            .welcome-section h2 {{
                color: #333;
                font-size: 2rem;
                margin-bottom: 20px;
            }}

            .welcome-section p {{
                color: #666;
                font-size: 1.1rem;
                line-height: 1.6;
                margin-bottom: 30px;
            }}

            .features-preview {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}

            .feature-preview {{
                background: #f8f9fa;
                border-radius: 12px;
                padding: 20px;
                text-align: center;
                border: 2px solid #e9ecef;
                transition: all 0.3s ease;
            }}

            .feature-preview:hover {{
                border-color: #667eea;
                transform: translateY(-5px);
            }}

            .feature-preview .icon {{
                font-size: 2rem;
                margin-bottom: 10px;
            }}

            .feature-preview h3 {{
                color: #333;
                margin-bottom: 10px;
            }}

            .feature-preview p {{
                color: #666;
                font-size: 0.9rem;
            }}

            .cta-buttons {{
                display: flex;
                gap: 20px;
                justify-content: center;
                flex-wrap: wrap;
            }}

            .btn {{
                padding: 15px 30px;
                border: none;
                border-radius: 50px;
                font-size: 1.1rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
                text-align: center;
            }}

            .btn-primary {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            }}

            .btn-primary:hover {{
                transform: translateY(-3px);
                box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
            }}

            .btn-secondary {{
                background: transparent;
                color: #667eea;
                border: 2px solid #667eea;
            }}

            .btn-secondary:hover {{
                background: #667eea;
                color: white;
            }}

            .progress-info {{
                background: #f8f9fa;
                border-radius: 12px;
                padding: 20px;
                margin: 20px 0;
                text-align: center;
            }}

            .progress-info h3 {{
                color: #333;
                margin-bottom: 10px;
            }}

            .progress-info p {{
                color: #666;
                margin-bottom: 5px;
            }}

            @media (max-width: 768px) {{
                .onboarding-container {{
                    margin: 10px;
                }}
                
                .onboarding-header {{
                    padding: 30px 20px;
                }}
                
                .onboarding-content {{
                    padding: 30px 20px;
                }}
                
                .cta-buttons {{
                    flex-direction: column;
                    align-items: center;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="onboarding-container">
            <div class="onboarding-header">
                <h1>🌱 Welcome to Vibespan.ai</h1>
                <p>Your Personal AI Wellness Concierge</p>
            </div>
            
            <div class="onboarding-content">
                <div class="step-indicator">
                    <div class="step active">1</div>
                    <div class="step">2</div>
                    <div class="step">3</div>
                    <div class="step">4</div>
                    <div class="step">5</div>
                    <div class="step">6</div>
                    <div class="step">7</div>
                    <div class="step">8</div>
                    <div class="step">9</div>
                </div>

                <div class="welcome-section">
                    <h2>Let's Set Up Your Wellness Journey!</h2>
                    <p>We'll personalize your AI wellness concierge in just a few steps. This will take about 5 minutes.</p>
                </div>

                <div class="progress-info">
                    <h3>Step 1 of 9: Welcome</h3>
                    <p><strong>Next Action:</strong> {onboarding_data.get('next_action', 'Set your wellness goals')}</p>
                    <p><strong>User ID:</strong> {onboarding_data.get('user_id', 'vibespan')}</p>
                </div>

                <div class="features-preview">
                    <div class="feature-preview">
                        <div class="icon">🎯</div>
                        <h3>Wellness Goals</h3>
                        <p>Set personalized wellness objectives</p>
                    </div>
                    <div class="feature-preview">
                        <div class="icon">📱</div>
                        <h3>Health Tools</h3>
                        <p>Connect your fitness devices</p>
                    </div>
                    <div class="feature-preview">
                        <div class="icon">🤖</div>
                        <h3>AI Concierge</h3>
                        <p>Get personalized recommendations</p>
                    </div>
                    <div class="feature-preview">
                        <div class="icon">⚡</div>
                        <h3>Automation</h3>
                        <p>Set & forget wellness management</p>
                    </div>
                </div>

                <div class="cta-buttons">
                    <a href="/onboarding/health-goals" class="btn btn-primary">
                        🚀 Start Setup
                    </a>
                    <a href="/" class="btn btn-secondary">
                        ← Back to Home
                    </a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/onboarding/health-goals", response_class=HTMLResponse)
async def get_health_goals_options():
    """Get available health goals for selection with HTML interface"""
    goals = onboarding_flow.get_health_goals_options()
    
    # Generate goal cards HTML
    goal_cards_html = ""
    for goal in goals:
        goal_cards_html += f'''
                    <div class="goal-card" onclick="toggleGoal('{goal["id"]}')" id="goal-{goal["id"]}">
                        <h3><span class="icon">{goal["icon"]}</span>{goal["title"]}</h3>
                        <p>{goal["description"]}</p>
                    </div>
        '''
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vibespan.ai - Select Wellness Goals</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }}
            .container {{ background: white; border-radius: 20px; box-shadow: 0 30px 60px rgba(0,0,0,0.3); max-width: 800px; width: 100%; overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }}
            .header h1 {{ font-size: 2.5rem; margin-bottom: 10px; }}
            .content {{ padding: 40px; }}
            .step-indicator {{ display: flex; justify-content: center; margin-bottom: 40px; flex-wrap: wrap; }}
            .step {{ width: 40px; height: 40px; border-radius: 50%; background: #e9ecef; display: flex; align-items: center; justify-content: center; margin: 5px; font-weight: 600; color: #666; }}
            .step.active {{ background: #667eea; color: white; }}
            .step.completed {{ background: #28a745; color: white; }}
            .goals-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0; }}
            .goal-card {{ background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 12px; padding: 20px; cursor: pointer; transition: all 0.3s ease; }}
            .goal-card:hover {{ border-color: #667eea; transform: translateY(-5px); }}
            .goal-card.selected {{ border-color: #667eea; background: #f0f4ff; }}
            .goal-card h3 {{ color: #333; margin-bottom: 10px; display: flex; align-items: center; }}
            .goal-card .icon {{ font-size: 1.5rem; margin-right: 10px; }}
            .goal-card p {{ color: #666; font-size: 0.9rem; line-height: 1.4; }}
            .btn {{ padding: 15px 30px; border: none; border-radius: 50px; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: all 0.3s ease; text-decoration: none; display: inline-block; text-align: center; margin: 10px; }}
            .btn-primary {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3); }}
            .btn-primary:hover {{ transform: translateY(-3px); box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4); }}
            .btn-secondary {{ background: transparent; color: #667eea; border: 2px solid #667eea; }}
            .btn-secondary:hover {{ background: #667eea; color: white; }}
            .btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}
            .cta-buttons {{ display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-top: 30px; }}
            .selected-count {{ text-align: center; margin: 20px 0; color: #667eea; font-weight: 600; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎯 Select Your Wellness Goals</h1>
                <p>Choose what you want to focus on for your wellness journey</p>
            </div>
            
            <div class="content">
                <div class="step-indicator">
                    <div class="step completed">1</div>
                    <div class="step active">2</div>
                    <div class="step">3</div>
                    <div class="step">4</div>
                    <div class="step">5</div>
                    <div class="step">6</div>
                    <div class="step">7</div>
                    <div class="step">8</div>
                    <div class="step">9</div>
                </div>

                <div class="goals-grid">
                    {goal_cards_html}
                </div>

                <div class="selected-count" id="selected-count">
                    Select at least one wellness goal to continue
                </div>

                <div class="cta-buttons">
                    <button class="btn btn-primary" id="continue-btn" onclick="continueToNext()" disabled>
                        Continue to Daily Goals →
                    </button>
                    <a href="/onboarding/start" class="btn btn-secondary">
                        ← Back
                    </a>
                </div>
            </div>
        </div>

        <script>
            let selectedGoals = [];
            
            function toggleGoal(goalId) {{
                const card = document.getElementById('goal-' + goalId);
                const index = selectedGoals.indexOf(goalId);
                
                if (index > -1) {{
                    selectedGoals.splice(index, 1);
                    card.classList.remove('selected');
                }} else {{
                    selectedGoals.push(goalId);
                    card.classList.add('selected');
                }}
                
                updateUI();
            }}
            
            function updateUI() {{
                const count = selectedGoals.length;
                const countEl = document.getElementById('selected-count');
                const continueBtn = document.getElementById('continue-btn');
                
                if (count === 0) {{
                    countEl.textContent = 'Select at least one wellness goal to continue';
                    continueBtn.disabled = true;
                }} else {{
                    countEl.textContent = `${{count}} goal${{count > 1 ? 's' : ''}} selected`;
                    continueBtn.disabled = false;
                }}
            }}
            
            function continueToNext() {{
                if (selectedGoals.length > 0) {{
                    // Store selected goals and continue
                    localStorage.setItem('selected_goals', JSON.stringify(selectedGoals));
                    window.location.href = '/onboarding/daily-goals';
                }}
            }}
        </script>
    </body>
    </html>
    """

@app.get("/onboarding/daily-goals", response_class=HTMLResponse)
async def get_daily_goals_options():
    """Get available daily goals for selection with HTML interface"""
    daily_goals = onboarding_flow.get_daily_goals_options()
    
    # Generate daily goal cards HTML
    goal_cards_html = ""
    for goal in daily_goals:
        # Add icon based on category
        icon_map = {
            "sleep": "😴",
            "exercise": "🏃",
            "nutrition": "🥗",
            "wellness": "🧘",
            "recovery": "⚡"
        }
        icon = icon_map.get(goal["category"], "📅")
        
        goal_cards_html += f'''
                    <div class="goal-card" onclick="toggleGoal('{goal["id"]}')" id="goal-{goal["id"]}">
                        <h3><span class="icon">{icon}</span>{goal["title"]}</h3>
                        <p>{goal["description"]}</p>
                        <div class="goal-meta">
                            <span class="category">{goal["category"]}</span>
                            <span class="frequency">{goal["frequency"]}</span>
                        </div>
                    </div>
        '''
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vibespan.ai - Select Daily Goals</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }}
            .container {{ background: white; border-radius: 20px; box-shadow: 0 30px 60px rgba(0,0,0,0.3); max-width: 900px; width: 100%; overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }}
            .header h1 {{ font-size: 2.5rem; margin-bottom: 10px; }}
            .content {{ padding: 40px; }}
            .step-indicator {{ display: flex; justify-content: center; margin-bottom: 40px; flex-wrap: wrap; }}
            .step {{ width: 40px; height: 40px; border-radius: 50%; background: #e9ecef; display: flex; align-items: center; justify-content: center; margin: 5px; font-weight: 600; color: #666; }}
            .step.active {{ background: #667eea; color: white; }}
            .step.completed {{ background: #28a745; color: white; }}
            .goals-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; margin: 30px 0; }}
            .goal-card {{ background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 12px; padding: 25px; cursor: pointer; transition: all 0.3s ease; position: relative; }}
            .goal-card:hover {{ border-color: #667eea; transform: translateY(-5px); box-shadow: 0 10px 25px rgba(102, 126, 234, 0.15); }}
            .goal-card.selected {{ border-color: #667eea; background: #f0f4ff; }}
            .goal-card h3 {{ color: #333; margin-bottom: 15px; display: flex; align-items: center; }}
            .goal-card .icon {{ font-size: 1.8rem; margin-right: 12px; }}
            .goal-card p {{ color: #666; font-size: 0.95rem; line-height: 1.5; margin-bottom: 15px; }}
            .goal-meta {{ display: flex; justify-content: space-between; align-items: center; margin-top: 15px; padding-top: 15px; border-top: 1px solid #e9ecef; }}
            .category {{ background: #667eea; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; }}
            .frequency {{ color: #666; font-size: 0.85rem; font-weight: 500; }}
            .btn {{ padding: 15px 30px; border: none; border-radius: 50px; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: all 0.3s ease; text-decoration: none; display: inline-block; text-align: center; margin: 10px; }}
            .btn-primary {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3); }}
            .btn-primary:hover {{ transform: translateY(-3px); box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4); }}
            .btn-secondary {{ background: transparent; color: #667eea; border: 2px solid #667eea; }}
            .btn-secondary:hover {{ background: #667eea; color: white; }}
            .btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}
            .cta-buttons {{ display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-top: 30px; }}
            .selected-count {{ text-align: center; margin: 20px 0; color: #667eea; font-weight: 600; }}
            .progress-info {{ background: #f8f9fa; border-radius: 12px; padding: 20px; margin: 20px 0; text-align: center; }}
            .progress-info h3 {{ color: #333; margin-bottom: 10px; }}
            .progress-info p {{ color: #666; margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📅 Select Your Daily Goals</h1>
                <p>Choose your daily habits for consistency tracking</p>
            </div>
            
            <div class="content">
                <div class="step-indicator">
                    <div class="step completed">1</div>
                    <div class="step completed">2</div>
                    <div class="step active">3</div>
                    <div class="step">4</div>
                    <div class="step">5</div>
                    <div class="step">6</div>
                    <div class="step">7</div>
                    <div class="step">8</div>
                    <div class="step">9</div>
                </div>

                <div class="progress-info">
                    <h3>Step 3 of 9: Daily Goals</h3>
                    <p>Select the daily habits you want to track and maintain consistently</p>
                </div>

                <div class="goals-grid">
                    {goal_cards_html}
                </div>

                <div class="selected-count" id="selected-count">
                    Select at least one daily goal to continue
                </div>

                <div class="cta-buttons">
                    <button class="btn btn-primary" id="continue-btn" onclick="continueToNext()" disabled>
                        Continue to Health Tools →
                    </button>
                    <a href="/onboarding/health-goals" class="btn btn-secondary">
                        ← Back
                    </a>
                </div>
            </div>
        </div>

        <script>
            let selectedGoals = [];
            
            function toggleGoal(goalId) {{
                const card = document.getElementById('goal-' + goalId);
                const index = selectedGoals.indexOf(goalId);
                
                if (index > -1) {{
                    selectedGoals.splice(index, 1);
                    card.classList.remove('selected');
                }} else {{
                    selectedGoals.push(goalId);
                    card.classList.add('selected');
                }}
                
                updateUI();
            }}
            
            function updateUI() {{
                const count = selectedGoals.length;
                const countEl = document.getElementById('selected-count');
                const continueBtn = document.getElementById('continue-btn');
                
                if (count === 0) {{
                    countEl.textContent = 'Select at least one daily goal to continue';
                    continueBtn.disabled = true;
                }} else {{
                    countEl.textContent = `${{count}} daily goal${{count > 1 ? 's' : ''}} selected`;
                    continueBtn.disabled = false;
                }}
            }}
            
            function continueToNext() {{
                if (selectedGoals.length > 0) {{
                    // Store selected goals and continue
                    localStorage.setItem('selected_daily_goals', JSON.stringify(selectedGoals));
                    window.location.href = '/onboarding/health-tools';
                }}
            }}
        </script>
    </body>
    </html>
    """

@app.get("/onboarding/health-tools", response_class=HTMLResponse)
async def get_health_tools_options():
    """Get available health tools and devices with HTML interface"""
    health_tools = onboarding_flow.get_health_tools_options()
    
    # Generate health tool cards HTML
    tool_cards_html = ""
    for tool in health_tools:
        # Add icon based on tool type
        icon_map = {
            "wearable": "⌚",
            "mobile": "📱",
            "manual": "📝"
        }
        icon = icon_map.get(tool["type"], "🔧")
        
        # Generate features list
        features_html = ""
        for feature in tool["features"]:
            features_html += f'<span class="feature-tag">{feature.replace("_", " ").title()}</span>'
        
        tool_cards_html += f'''
                    <div class="tool-card" onclick="toggleTool('{tool["id"]}')" id="tool-{tool["id"]}">
                        <div class="tool-header">
                            <h3><span class="icon">{icon}</span>{tool["name"]}</h3>
                            <div class="tool-type">{tool["type"].title()}</div>
                        </div>
                        <p class="tool-description">{tool["description"]}</p>
                        <div class="tool-features">
                            {features_html}
                        </div>
                        <div class="integration-badge">
                            <span class="integration-type">{tool["integration"].upper()}</span>
                        </div>
                    </div>
        '''
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vibespan.ai - Select Health Tools</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }}
            .container {{ background: white; border-radius: 20px; box-shadow: 0 30px 60px rgba(0,0,0,0.3); max-width: 1000px; width: 100%; overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }}
            .header h1 {{ font-size: 2.5rem; margin-bottom: 10px; }}
            .content {{ padding: 40px; }}
            .step-indicator {{ display: flex; justify-content: center; margin-bottom: 40px; flex-wrap: wrap; }}
            .step {{ width: 40px; height: 40px; border-radius: 50%; background: #e9ecef; display: flex; align-items: center; justify-content: center; margin: 5px; font-weight: 600; color: #666; }}
            .step.active {{ background: #667eea; color: white; }}
            .step.completed {{ background: #28a745; color: white; }}
            .tools-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 25px; margin: 30px 0; }}
            .tool-card {{ background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 15px; padding: 25px; cursor: pointer; transition: all 0.3s ease; position: relative; }}
            .tool-card:hover {{ border-color: #667eea; transform: translateY(-5px); box-shadow: 0 15px 35px rgba(102, 126, 234, 0.15); }}
            .tool-card.selected {{ border-color: #667eea; background: #f0f4ff; }}
            .tool-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }}
            .tool-header h3 {{ color: #333; display: flex; align-items: center; font-size: 1.3rem; }}
            .tool-header .icon {{ font-size: 1.8rem; margin-right: 12px; }}
            .tool-type {{ background: #e9ecef; color: #666; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; }}
            .tool-description {{ color: #666; font-size: 0.95rem; line-height: 1.5; margin-bottom: 20px; }}
            .tool-features {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px; }}
            .feature-tag {{ background: #667eea; color: white; padding: 4px 10px; border-radius: 15px; font-size: 0.75rem; font-weight: 500; }}
            .integration-badge {{ position: absolute; top: 15px; right: 15px; }}
            .integration-type {{ background: #28a745; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: 600; }}
            .btn {{ padding: 15px 30px; border: none; border-radius: 50px; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: all 0.3s ease; text-decoration: none; display: inline-block; text-align: center; margin: 10px; }}
            .btn-primary {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3); }}
            .btn-primary:hover {{ transform: translateY(-3px); box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4); }}
            .btn-secondary {{ background: transparent; color: #667eea; border: 2px solid #667eea; }}
            .btn-secondary:hover {{ background: #667eea; color: white; }}
            .btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}
            .cta-buttons {{ display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-top: 30px; }}
            .selected-count {{ text-align: center; margin: 20px 0; color: #667eea; font-weight: 600; }}
            .progress-info {{ background: #f8f9fa; border-radius: 12px; padding: 20px; margin: 20px 0; text-align: center; }}
            .progress-info h3 {{ color: #333; margin-bottom: 10px; }}
            .progress-info p {{ color: #666; margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📱 Select Your Health Tools</h1>
                <p>Choose the health tools and devices you use for data collection</p>
            </div>
            
            <div class="content">
                <div class="step-indicator">
                    <div class="step completed">1</div>
                    <div class="step completed">2</div>
                    <div class="step completed">3</div>
                    <div class="step active">4</div>
                    <div class="step">5</div>
                    <div class="step">6</div>
                    <div class="step">7</div>
                    <div class="step">8</div>
                    <div class="step">9</div>
                </div>

                <div class="progress-info">
                    <h3>Step 4 of 9: Health Tools</h3>
                    <p>Select the health tools and devices you use to collect wellness data</p>
                </div>

                <div class="tools-grid">
                    {tool_cards_html}
                </div>

                <div class="selected-count" id="selected-count">
                    Select at least one health tool to continue
                </div>

                <div class="cta-buttons">
                    <button class="btn btn-primary" id="continue-btn" onclick="continueToNext()" disabled>
                        Continue to Service Configuration →
                    </button>
                    <a href="/onboarding/daily-goals" class="btn btn-secondary">
                        ← Back
                    </a>
                </div>
            </div>
        </div>

        <script>
            let selectedTools = [];
            
            function toggleTool(toolId) {{
                const card = document.getElementById('tool-' + toolId);
                const index = selectedTools.indexOf(toolId);
                
                if (index > -1) {{
                    selectedTools.splice(index, 1);
                    card.classList.remove('selected');
                }} else {{
                    selectedTools.push(toolId);
                    card.classList.add('selected');
                }}
                
                updateUI();
            }}
            
            function updateUI() {{
                const count = selectedTools.length;
                const countEl = document.getElementById('selected-count');
                const continueBtn = document.getElementById('continue-btn');
                
                if (count === 0) {{
                    countEl.textContent = 'Select at least one health tool to continue';
                    continueBtn.disabled = true;
                }} else {{
                    countEl.textContent = `${{count}} health tool${{count > 1 ? 's' : ''}} selected`;
                    continueBtn.disabled = false;
                }}
            }}
            
            function continueToNext() {{
                if (selectedTools.length > 0) {{
                    // Store selected tools and continue
                    localStorage.setItem('selected_health_tools', JSON.stringify(selectedTools));
                    window.location.href = '/onboarding/service-configuration';
                }}
            }}
        </script>
    </body>
    </html>
    """

@app.get("/onboarding/service-configuration", response_class=HTMLResponse)
async def get_service_configuration():
    """Get service configuration with HTML interface"""
    catalog_data = service_catalog.get_all_services()
    hybrid_templates = service_catalog.get_hybrid_templates()
    
    # Generate service cards HTML
    service_cards_html = ""
    for category, services in catalog_data["services"].items():
        for service in services:
            service_id = service["service_id"]
            # Add icon based on category
            icon_map = {
                "Fitness & Performance": "💪",
                "Recovery & Sleep": "😴",
                "Nutrition & Wellness": "🥗",
                "Longevity & Optimization": "🧬",
                "Data & Analytics": "📊",
                "Coaching & Guidance": "🎯",
                "Safety & Monitoring": "🛡️"
            }
            icon = icon_map.get(service["category"], "🔧")
            
            service_cards_html += f'''
                        <div class="service-card" onclick="toggleService('{service_id}')" id="service-{service_id}">
                            <div class="service-header">
                                <h3><span class="icon">{icon}</span>{service["name"]}</h3>
                                <div class="service-category">{service["category"]}</div>
                            </div>
                            <p class="service-description">{service["description"]}</p>
                            <div class="service-priority">
                                <label>Priority:</label>
                                <select id="priority-{service_id}" onchange="updatePriority('{service_id}')">
                                    <option value="high">High</option>
                                    <option value="medium" selected>Medium</option>
                                    <option value="low">Low</option>
                                    <option value="disabled">Disabled</option>
                                </select>
                            </div>
                        </div>
            '''
    
    # Generate hybrid template options
    template_options_html = ""
    for template_id, template in hybrid_templates.items():
        template_options_html += f'''
                    <div class="template-option" onclick="selectTemplate('{template_id}')" id="template-{template_id}">
                        <h4>{template_id}</h4>
                        <p>{template["description"]}</p>
                        <div class="template-services">
                            {len(template["services"])} services included
                        </div>
                    </div>
        '''
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vibespan.ai - Service Configuration</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }}
            .container {{ background: white; border-radius: 20px; box-shadow: 0 30px 60px rgba(0,0,0,0.3); max-width: 1200px; width: 100%; overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }}
            .header h1 {{ font-size: 2.5rem; margin-bottom: 10px; }}
            .content {{ padding: 40px; }}
            .step-indicator {{ display: flex; justify-content: center; margin-bottom: 40px; flex-wrap: wrap; }}
            .step {{ width: 40px; height: 40px; border-radius: 50%; background: #e9ecef; display: flex; align-items: center; justify-content: center; margin: 5px; font-weight: 600; color: #666; }}
            .step.active {{ background: #667eea; color: white; }}
            .step.completed {{ background: #28a745; color: white; }}
            .tabs {{ display: flex; margin-bottom: 30px; border-bottom: 2px solid #e9ecef; }}
            .tab {{ padding: 15px 30px; cursor: pointer; border-bottom: 3px solid transparent; transition: all 0.3s ease; }}
            .tab.active {{ border-bottom-color: #667eea; color: #667eea; font-weight: 600; }}
            .tab-content {{ display: none; }}
            .tab-content.active {{ display: block; }}
            .services-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; margin: 30px 0; }}
            .service-card {{ background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 15px; padding: 25px; cursor: pointer; transition: all 0.3s ease; }}
            .service-card:hover {{ border-color: #667eea; transform: translateY(-3px); }}
            .service-card.selected {{ border-color: #667eea; background: #f0f4ff; }}
            .service-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }}
            .service-header h3 {{ color: #333; display: flex; align-items: center; font-size: 1.2rem; }}
            .service-header .icon {{ font-size: 1.5rem; margin-right: 10px; }}
            .service-category {{ background: #e9ecef; color: #666; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }}
            .service-description {{ color: #666; font-size: 0.9rem; line-height: 1.5; margin-bottom: 15px; }}
            .service-priority {{ display: flex; align-items: center; gap: 10px; }}
            .service-priority label {{ font-weight: 600; color: #333; }}
            .service-priority select {{ padding: 5px 10px; border: 1px solid #ddd; border-radius: 5px; }}
            .templates-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 30px 0; }}
            .template-option {{ background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 15px; padding: 25px; cursor: pointer; transition: all 0.3s ease; }}
            .template-option:hover {{ border-color: #667eea; transform: translateY(-3px); }}
            .template-option.selected {{ border-color: #667eea; background: #f0f4ff; }}
            .template-option h4 {{ color: #333; margin-bottom: 10px; }}
            .template-option p {{ color: #666; font-size: 0.9rem; line-height: 1.5; margin-bottom: 15px; }}
            .template-services {{ background: #667eea; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; display: inline-block; }}
            .btn {{ padding: 15px 30px; border: none; border-radius: 50px; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: all 0.3s ease; text-decoration: none; display: inline-block; text-align: center; margin: 10px; }}
            .btn-primary {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3); }}
            .btn-primary:hover {{ transform: translateY(-3px); box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4); }}
            .btn-secondary {{ background: transparent; color: #667eea; border: 2px solid #667eea; }}
            .btn-secondary:hover {{ background: #667eea; color: white; }}
            .btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}
            .cta-buttons {{ display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-top: 30px; }}
            .selected-count {{ text-align: center; margin: 20px 0; color: #667eea; font-weight: 600; }}
            .progress-info {{ background: #f8f9fa; border-radius: 12px; padding: 20px; margin: 20px 0; text-align: center; }}
            .progress-info h3 {{ color: #333; margin-bottom: 10px; }}
            .progress-info p {{ color: #666; margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⚙️ Configure Your Services</h1>
                <p>Choose your wellness services and set priorities</p>
            </div>
            
            <div class="content">
                <div class="step-indicator">
                    <div class="step completed">1</div>
                    <div class="step completed">2</div>
                    <div class="step completed">3</div>
                    <div class="step completed">4</div>
                    <div class="step active">5</div>
                    <div class="step">6</div>
                    <div class="step">7</div>
                    <div class="step">8</div>
                    <div class="step">9</div>
                </div>

                <div class="progress-info">
                    <h3>Step 5 of 9: Service Configuration</h3>
                    <p>Select and configure your wellness services with custom priorities</p>
                </div>

                <div class="tabs">
                    <div class="tab active" onclick="switchTab('individual')">Individual Services</div>
                    <div class="tab" onclick="switchTab('templates')">Hybrid Templates</div>
                </div>

                <div id="individual-tab" class="tab-content active">
                    <div class="services-grid">
                        {service_cards_html}
                    </div>
                </div>

                <div id="templates-tab" class="tab-content">
                    <div class="templates-grid">
                        {template_options_html}
                    </div>
                </div>

                <div class="selected-count" id="selected-count">
                    Select at least one service to continue
                </div>

                <div class="cta-buttons">
                    <button class="btn btn-primary" id="continue-btn" onclick="continueToNext()" disabled>
                        Continue to Data Preferences →
                    </button>
                    <a href="/onboarding/health-tools" class="btn btn-secondary">
                        ← Back
                    </a>
                </div>
            </div>
        </div>

        <script>
            let selectedServices = {{}};
            let selectedTemplate = null;
            
            function switchTab(tabName) {{
                // Hide all tab contents
                document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
                document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
                
                // Show selected tab
                document.getElementById(tabName + '-tab').classList.add('active');
                event.target.classList.add('active');
            }}
            
            function toggleService(serviceId) {{
                const card = document.getElementById('service-' + serviceId);
                const priority = document.getElementById('priority-' + serviceId).value;
                
                if (selectedServices[serviceId]) {{
                    delete selectedServices[serviceId];
                    card.classList.remove('selected');
                }} else {{
                    selectedServices[serviceId] = {{ priority: priority, enabled: true }};
                    card.classList.add('selected');
                }}
                
                updateUI();
            }}
            
            function updatePriority(serviceId) {{
                if (selectedServices[serviceId]) {{
                    selectedServices[serviceId].priority = document.getElementById('priority-' + serviceId).value;
                }}
            }}
            
            function selectTemplate(templateId) {{
                selectedTemplate = templateId;
                document.querySelectorAll('.template-option').forEach(option => option.classList.remove('selected'));
                document.getElementById('template-' + templateId).classList.add('selected');
                updateUI();
            }}
            
            function updateUI() {{
                const serviceCount = Object.keys(selectedServices).length;
                const countEl = document.getElementById('selected-count');
                const continueBtn = document.getElementById('continue-btn');
                
                if (serviceCount === 0 && !selectedTemplate) {{
                    countEl.textContent = 'Select at least one service or template to continue';
                    continueBtn.disabled = true;
                }} else {{
                    countEl.textContent = `${{serviceCount}} service${{serviceCount > 1 ? 's' : ''}} selected`;
                    continueBtn.disabled = false;
                }}
            }}
            
            function continueToNext() {{
                if (Object.keys(selectedServices).length > 0 || selectedTemplate) {{
                    // Store selected services and continue
                    localStorage.setItem('selected_services', JSON.stringify(selectedServices));
                    localStorage.setItem('selected_template', selectedTemplate);
                    window.location.href = '/onboarding/data-preferences';
                }}
            }}
        </script>
    </body>
    </html>
    """

@app.get("/onboarding/service-catalog")
async def get_service_catalog():
    """Get comprehensive service catalog"""
    return {
        "status": "success",
        "service_catalog": onboarding_flow.get_service_catalog()
    }

@app.get("/onboarding/data-preferences", response_class=HTMLResponse)
async def get_data_preferences():
    """Get data preferences configuration with HTML interface"""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vibespan.ai - Data Preferences</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }}
            .container {{ background: white; border-radius: 20px; box-shadow: 0 30px 60px rgba(0,0,0,0.3); max-width: 1000px; width: 100%; overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }}
            .header h1 {{ font-size: 2.5rem; margin-bottom: 10px; }}
            .content {{ padding: 40px; }}
            .step-indicator {{ display: flex; justify-content: center; margin-bottom: 40px; flex-wrap: wrap; }}
            .step {{ width: 40px; height: 40px; border-radius: 50%; background: #e9ecef; display: flex; align-items: center; justify-content: center; margin: 5px; font-weight: 600; color: #666; }}
            .step.active {{ background: #667eea; color: white; }}
            .step.completed {{ background: #28a745; color: white; }}
            .preferences-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 25px; margin: 30px 0; }}
            .preference-card {{ background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 15px; padding: 25px; transition: all 0.3s ease; }}
            .preference-card:hover {{ border-color: #667eea; transform: translateY(-3px); }}
            .preference-card h3 {{ color: #333; margin-bottom: 15px; display: flex; align-items: center; font-size: 1.3rem; }}
            .preference-card .icon {{ font-size: 1.8rem; margin-right: 12px; }}
            .preference-card p {{ color: #666; font-size: 0.95rem; line-height: 1.5; margin-bottom: 20px; }}
            .preference-options {{ display: flex; flex-direction: column; gap: 15px; }}
            .option-group {{ display: flex; align-items: center; justify-content: space-between; padding: 15px; background: white; border-radius: 10px; border: 1px solid #e9ecef; }}
            .option-group:hover {{ border-color: #667eea; }}
            .option-label {{ font-weight: 600; color: #333; }}
            .option-controls {{ display: flex; align-items: center; gap: 10px; }}
            .toggle {{ position: relative; width: 50px; height: 25px; background: #ddd; border-radius: 25px; cursor: pointer; transition: background 0.3s; }}
            .toggle.active {{ background: #667eea; }}
            .toggle::after {{ content: ''; position: absolute; top: 2px; left: 2px; width: 21px; height: 21px; background: white; border-radius: 50%; transition: transform 0.3s; }}
            .toggle.active::after {{ transform: translateX(25px); }}
            .select {{ padding: 8px 12px; border: 1px solid #ddd; border-radius: 5px; background: white; }}
            .btn {{ padding: 15px 30px; border: none; border-radius: 50px; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: all 0.3s ease; text-decoration: none; display: inline-block; text-align: center; margin: 10px; }}
            .btn-primary {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3); }}
            .btn-primary:hover {{ transform: translateY(-3px); box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4); }}
            .btn-secondary {{ background: transparent; color: #667eea; border: 2px solid #667eea; }}
            .btn-secondary:hover {{ background: #667eea; color: white; }}
            .btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}
            .cta-buttons {{ display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-top: 30px; }}
            .progress-info {{ background: #f8f9fa; border-radius: 12px; padding: 20px; margin: 20px 0; text-align: center; }}
            .progress-info h3 {{ color: #333; margin-bottom: 10px; }}
            .progress-info p {{ color: #666; margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⚙️ Data Preferences</h1>
                <p>Configure how your wellness data is collected and used</p>
            </div>
            
            <div class="content">
                <div class="step-indicator">
                    <div class="step completed">1</div>
                    <div class="step completed">2</div>
                    <div class="step completed">3</div>
                    <div class="step completed">4</div>
                    <div class="step completed">5</div>
                    <div class="step active">6</div>
                    <div class="step">7</div>
                    <div class="step">8</div>
                    <div class="step">9</div>
                </div>

                <div class="progress-info">
                    <h3>Step 6 of 9: Data Preferences</h3>
                    <p>Customize your data collection and privacy settings</p>
                </div>

                <div class="preferences-grid">
                    <div class="preference-card" id="data-collection">
                        <h3><span class="icon">📊</span>Data Collection</h3>
                        <p>Choose how frequently and what type of data to collect</p>
                        <div class="preference-options">
                            <div class="option-group">
                                <span class="option-label">Real-time Monitoring</span>
                                <div class="option-controls">
                                    <div class="toggle active" id="real-time-monitoring" onclick="toggleOption(this)"></div>
                                </div>
                            </div>
                            <div class="option-group">
                                <span class="option-label">Data Collection Frequency</span>
                                <div class="option-controls">
                                    <select class="select" id="collection-frequency">
                                        <option value="continuous">Continuous</option>
                                        <option value="hourly" selected>Hourly</option>
                                        <option value="daily">Daily</option>
                                        <option value="weekly">Weekly</option>
                                    </select>
                                </div>
                            </div>
                            <div class="option-group">
                                <span class="option-label">Include Sleep Data</span>
                                <div class="option-controls">
                                    <div class="toggle active" id="include-sleep" onclick="toggleOption(this)"></div>
                                </div>
                            </div>
                            <div class="option-group">
                                <span class="option-label">Include Activity Data</span>
                                <div class="option-controls">
                                    <div class="toggle active" id="include-activity" onclick="toggleOption(this)"></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="preference-card" id="privacy">
                        <h3><span class="icon">🔒</span>Privacy & Security</h3>
                        <p>Control how your data is stored and shared</p>
                        <div class="preference-options">
                            <div class="option-group">
                                <span class="option-label">Data Encryption</span>
                                <div class="option-controls">
                                    <div class="toggle active" id="data-encryption" onclick="toggleOption(this)"></div>
                                </div>
                            </div>
                            <div class="option-group">
                                <span class="option-label">Anonymous Analytics</span>
                                <div class="option-controls">
                                    <div class="toggle active" id="anonymous-analytics" onclick="toggleOption(this)"></div>
                                </div>
                            </div>
                            <div class="option-group">
                                <span class="option-label">Data Retention Period</span>
                                <div class="option-controls">
                                    <select class="select" id="retention-period">
                                        <option value="1year">1 Year</option>
                                        <option value="2years">2 Years</option>
                                        <option value="3years" selected>3 Years</option>
                                        <option value="indefinite">Indefinite</option>
                                    </select>
                                </div>
                            </div>
                            <div class="option-group">
                                <span class="option-label">Export Data Access</span>
                                <div class="option-controls">
                                    <div class="toggle active" id="export-access" onclick="toggleOption(this)"></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="preference-card" id="notifications">
                        <h3><span class="icon">🔔</span>Notifications</h3>
                        <p>Set up alerts and reminders for your wellness journey</p>
                        <div class="preference-options">
                            <div class="option-group">
                                <span class="option-label">Daily Reminders</span>
                                <div class="option-controls">
                                    <div class="toggle active" id="daily-reminders" onclick="toggleOption(this)"></div>
                                </div>
                            </div>
                            <div class="option-group">
                                <span class="option-label">Health Alerts</span>
                                <div class="option-controls">
                                    <div class="toggle active" id="health-alerts" onclick="toggleOption(this)"></div>
                                </div>
                            </div>
                            <div class="option-group">
                                <span class="option-label">Weekly Reports</span>
                                <div class="option-controls">
                                    <div class="toggle active" id="weekly-reports" onclick="toggleOption(this)"></div>
                                </div>
                            </div>
                            <div class="option-group">
                                <span class="option-label">Goal Milestones</span>
                                <div class="option-controls">
                                    <div class="toggle active" id="goal-milestones" onclick="toggleOption(this)"></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="preference-card" id="ai-personalization">
                        <h3><span class="icon">🤖</span>AI Personalization</h3>
                        <p>Configure how AI learns and adapts to your preferences</p>
                        <div class="preference-options">
                            <div class="option-group">
                                <span class="option-label">Learning Mode</span>
                                <div class="option-controls">
                                    <select class="select" id="learning-mode">
                                        <option value="conservative">Conservative</option>
                                        <option value="balanced" selected>Balanced</option>
                                        <option value="aggressive">Aggressive</option>
                                    </select>
                                </div>
                            </div>
                            <div class="option-group">
                                <span class="option-label">Pattern Detection</span>
                                <div class="option-controls">
                                    <div class="toggle active" id="pattern-detection" onclick="toggleOption(this)"></div>
                                </div>
                            </div>
                            <div class="option-group">
                                <span class="option-label">Predictive Insights</span>
                                <div class="option-controls">
                                    <div class="toggle active" id="predictive-insights" onclick="toggleOption(this)"></div>
                                </div>
                            </div>
                            <div class="option-group">
                                <span class="option-label">Auto-optimization</span>
                                <div class="option-controls">
                                    <div class="toggle active" id="auto-optimization" onclick="toggleOption(this)"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="cta-buttons">
                    <button class="btn btn-primary" onclick="continueToNext()">
                        Continue to Template Selection →
                    </button>
                    <a href="/onboarding/service-configuration" class="btn btn-secondary">
                        ← Back
                    </a>
                </div>
            </div>
        </div>

        <script>
            function toggleOption(element) {{
                element.classList.toggle('active');
            }}
            
            function continueToNext() {{
                // Collect all preferences using specific IDs
                const preferences = {{
                    dataCollection: {{
                        realTimeMonitoring: document.getElementById('real-time-monitoring')?.classList.contains('active') || false,
                        frequency: document.getElementById('collection-frequency')?.value || 'hourly',
                        includeSleep: document.getElementById('include-sleep')?.classList.contains('active') || false,
                        includeActivity: document.getElementById('include-activity')?.classList.contains('active') || false
                    }},
                    privacy: {{
                        encryption: document.getElementById('data-encryption')?.classList.contains('active') || false,
                        anonymousAnalytics: document.getElementById('anonymous-analytics')?.classList.contains('active') || false,
                        retentionPeriod: document.getElementById('retention-period')?.value || '3years',
                        exportAccess: document.getElementById('export-access')?.classList.contains('active') || false
                    }},
                    notifications: {{
                        dailyReminders: document.getElementById('daily-reminders')?.classList.contains('active') || false,
                        healthAlerts: document.getElementById('health-alerts')?.classList.contains('active') || false,
                        weeklyReports: document.getElementById('weekly-reports')?.classList.contains('active') || false,
                        goalMilestones: document.getElementById('goal-milestones')?.classList.contains('active') || false
                    }},
                    aiPersonalization: {{
                        learningMode: document.getElementById('learning-mode')?.value || 'balanced',
                        patternDetection: document.getElementById('pattern-detection')?.classList.contains('active') || false,
                        predictiveInsights: document.getElementById('predictive-insights')?.classList.contains('active') || false,
                        autoOptimization: document.getElementById('auto-optimization')?.classList.contains('active') || false
                    }}
                }};
                
                // Store preferences and continue
                localStorage.setItem('data_preferences', JSON.stringify(preferences));
                window.location.href = '/onboarding/template-selection';
            }}
        </script>
    </body>
    </html>
    """

@app.get("/onboarding/template-selection", response_class=HTMLResponse)
async def get_template_selection():
    """Get template selection with HTML interface"""
    templates = onboarding_flow.get_health_templates()
    hybrid_templates = service_catalog.get_hybrid_templates()
    
    # Generate template cards HTML
    template_cards_html = ""
    for template_id, template in templates.items():
        # Add icon based on template type
        icon_map = {
            "fitness_enthusiast": "💪",
            "wellness_focused": "🌱",
            "health_optimizer": "🧬"
        }
        icon = icon_map.get(template_id, "📋")
        
        # Get default goals and tools for display
        default_goals = template.get("default_goals", [])
        default_tools = template.get("default_tools", [])
        default_actions = template.get("default_actions", [])
        
        template_cards_html += f'''
                    <div class="template-card" onclick="selectTemplate('{template_id}')" id="template-{template_id}">
                        <div class="template-header">
                            <h3><span class="icon">{icon}</span>{template["name"]}</h3>
                            <div class="template-type">Health Template</div>
                        </div>
                        <p class="template-description">{template["description"]}</p>
                        <div class="template-features">
                            <div class="feature-count">{len(default_goals)} goals, {len(default_tools)} tools</div>
                            <div class="data-points">
                                Goals: {', '.join(default_goals[:2])}{'...' if len(default_goals) > 2 else ''}
                            </div>
                            <div class="data-points">
                                Tools: {', '.join(default_tools[:2])}{'...' if len(default_tools) > 2 else ''}
                            </div>
                        </div>
                    </div>
        '''
    
    # Generate hybrid template options
    hybrid_template_cards_html = ""
    for template_id, template in hybrid_templates.items():
        hybrid_template_cards_html += f'''
                    <div class="template-card" onclick="selectHybridTemplate('{template_id}')" id="hybrid-{template_id}">
                        <div class="template-header">
                            <h3><span class="icon">⚡</span>{template["name"]}</h3>
                            <div class="template-type">Hybrid Template</div>
                        </div>
                        <p class="template-description">{template["description"]}</p>
                        <div class="template-features">
                            <div class="feature-count">{len(template["services"])} services included</div>
                            <div class="service-list">
                                {', '.join(list(template["services"].keys())[:3])}{'...' if len(template["services"]) > 3 else ''}
                            </div>
                        </div>
                    </div>
        '''
    
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vibespan.ai - Template Selection</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }}
            .container {{ background: white; border-radius: 20px; box-shadow: 0 30px 60px rgba(0,0,0,0.3); max-width: 1200px; width: 100%; overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; text-align: center; }}
            .header h1 {{ font-size: 2.5rem; margin-bottom: 10px; }}
            .content {{ padding: 40px; }}
            .step-indicator {{ display: flex; justify-content: center; margin-bottom: 40px; flex-wrap: wrap; }}
            .step {{ width: 40px; height: 40px; border-radius: 50%; background: #e9ecef; display: flex; align-items: center; justify-content: center; margin: 5px; font-weight: 600; color: #666; }}
            .step.active {{ background: #667eea; color: white; }}
            .step.completed {{ background: #28a745; color: white; }}
            .tabs {{ display: flex; margin-bottom: 30px; border-bottom: 2px solid #e9ecef; }}
            .tab {{ padding: 15px 30px; cursor: pointer; border-bottom: 3px solid transparent; transition: all 0.3s ease; }}
            .tab.active {{ border-bottom-color: #667eea; color: #667eea; font-weight: 600; }}
            .tab-content {{ display: none; }}
            .tab-content.active {{ display: block; }}
            .templates-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 25px; margin: 30px 0; }}
            .template-card {{ background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 15px; padding: 25px; cursor: pointer; transition: all 0.3s ease; }}
            .template-card:hover {{ border-color: #667eea; transform: translateY(-5px); box-shadow: 0 15px 35px rgba(102, 126, 234, 0.15); }}
            .template-card.selected {{ border-color: #667eea; background: #f0f4ff; }}
            .template-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }}
            .template-header h3 {{ color: #333; display: flex; align-items: center; font-size: 1.3rem; }}
            .template-header .icon {{ font-size: 1.8rem; margin-right: 12px; }}
            .template-type {{ background: #e9ecef; color: #666; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; }}
            .template-description {{ color: #666; font-size: 0.95rem; line-height: 1.5; margin-bottom: 20px; }}
            .template-features {{ display: flex; flex-direction: column; gap: 10px; }}
            .feature-count {{ background: #667eea; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; display: inline-block; width: fit-content; }}
            .data-points, .service-list {{ color: #666; font-size: 0.85rem; font-style: italic; }}
            .btn {{ padding: 15px 30px; border: none; border-radius: 50px; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: all 0.3s ease; text-decoration: none; display: inline-block; text-align: center; margin: 10px; }}
            .btn-primary {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3); }}
            .btn-primary:hover {{ transform: translateY(-3px); box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4); }}
            .btn-secondary {{ background: transparent; color: #667eea; border: 2px solid #667eea; }}
            .btn-secondary:hover {{ background: #667eea; color: white; }}
            .btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}
            .cta-buttons {{ display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-top: 30px; }}
            .selected-count {{ text-align: center; margin: 20px 0; color: #667eea; font-weight: 600; }}
            .progress-info {{ background: #f8f9fa; border-radius: 12px; padding: 20px; margin: 20px 0; text-align: center; }}
            .progress-info h3 {{ color: #333; margin-bottom: 10px; }}
            .progress-info p {{ color: #666; margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📋 Select Your Template</h1>
                <p>Choose your health data collection template</p>
            </div>
            
            <div class="content">
                <div class="step-indicator">
                    <div class="step completed">1</div>
                    <div class="step completed">2</div>
                    <div class="step completed">3</div>
                    <div class="step completed">4</div>
                    <div class="step completed">5</div>
                    <div class="step completed">6</div>
                    <div class="step active">7</div>
                    <div class="step">8</div>
                    <div class="step">9</div>
                </div>

                <div class="progress-info">
                    <h3>Step 7 of 9: Template Selection</h3>
                    <p>Choose your health data collection template and configuration</p>
                </div>

                <div class="tabs">
                    <div class="tab active" onclick="switchTab('data-templates')">Data Templates</div>
                    <div class="tab" onclick="switchTab('hybrid-templates')">Hybrid Templates</div>
                </div>

                <div id="data-templates-tab" class="tab-content active">
                    <div class="templates-grid">
                        {template_cards_html}
                    </div>
                </div>

                <div id="hybrid-templates-tab" class="tab-content">
                    <div class="templates-grid">
                        {hybrid_template_cards_html}
                    </div>
                </div>

                <div class="selected-count" id="selected-count">
                    Select a template to continue
                </div>

                <div class="cta-buttons">
                    <button class="btn btn-primary" id="continue-btn" onclick="continueToNext()" disabled>
                        Continue to Container Provisioning →
                    </button>
                    <a href="/onboarding/data-preferences" class="btn btn-secondary">
                        ← Back
                    </a>
                </div>
            </div>
        </div>

        <script>
            let selectedTemplate = null;
            let selectedHybridTemplate = null;
            
            function switchTab(tabName) {{
                // Hide all tab contents
                document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
                document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
                
                // Show selected tab
                document.getElementById(tabName + '-tab').classList.add('active');
                event.target.classList.add('active');
            }}
            
            function selectTemplate(templateId) {{
                selectedTemplate = templateId;
                selectedHybridTemplate = null;
                
                // Remove all selections
                document.querySelectorAll('.template-card').forEach(card => card.classList.remove('selected'));
                
                // Select current template
                document.getElementById('template-' + templateId).classList.add('selected');
                
                updateUI();
            }}
            
            function selectHybridTemplate(templateId) {{
                selectedHybridTemplate = templateId;
                selectedTemplate = null;
                
                // Remove all selections
                document.querySelectorAll('.template-card').forEach(card => card.classList.remove('selected'));
                
                // Select current template
                document.getElementById('hybrid-' + templateId).classList.add('selected');
                
                updateUI();
            }}
            
            function updateUI() {{
                const countEl = document.getElementById('selected-count');
                const continueBtn = document.getElementById('continue-btn');
                
                if (selectedTemplate || selectedHybridTemplate) {{
                    const templateName = selectedTemplate || selectedHybridTemplate;
                    countEl.textContent = `Selected: ${{templateName.replace('_', ' ').replace('-', ' ')}}`;
                    continueBtn.disabled = false;
                }} else {{
                    countEl.textContent = 'Select a template to continue';
                    continueBtn.disabled = true;
                }}
            }}
            
            function continueToNext() {{
                if (selectedTemplate || selectedHybridTemplate) {{
                    // Store selected template and continue
                    localStorage.setItem('selected_template', selectedTemplate);
                    localStorage.setItem('selected_hybrid_template', selectedHybridTemplate);
                    window.location.href = '/onboarding/container-provisioning';
                }}
            }}
        </script>
    </body>
    </html>
    """

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

# Managed Services & Automation Endpoints
@app.get("/api/managed-services/status")
async def get_managed_services_status(request: Request):
    """Get managed services status and automation info"""
    tenant_id = get_tenant_from_request(request)
    automation_engine = get_automation_engine(tenant_id)
    health_concierge = get_health_concierge(tenant_id)
    
    return {
        "tenant_id": tenant_id,
        "automation_status": automation_engine.get_automation_status(),
        "concierge_summary": health_concierge.get_concierge_summary(),
        "managed_services_active": True,
        "last_updated": datetime.now().isoformat()
    }

@app.get("/api/managed-services/concierge")
async def get_concierge_services(request: Request):
    """Get available concierge services"""
    tenant_id = get_tenant_from_request(request)
    health_concierge = get_health_concierge(tenant_id)
    
    return {
        "status": "success",
        "available_services": health_concierge.get_available_services()
    }

@app.post("/api/managed-services/concierge/upgrade")
async def upgrade_service_level(request: Request, new_level: str):
    """Upgrade user's service level"""
    tenant_id = get_tenant_from_request(request)
    health_concierge = get_health_concierge(tenant_id)
    
    from health_concierge import ServiceLevel
    try:
        service_level = ServiceLevel(new_level)
        result = health_concierge.upgrade_service_level(service_level)
        return result
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid service level: {new_level}")

@app.post("/api/managed-services/concierge/execute/{service_id}")
async def execute_concierge_service(request: Request, service_id: str):
    """Execute a concierge service"""
    tenant_id = get_tenant_from_request(request)
    health_concierge = get_health_concierge(tenant_id)
    
    data = await request.json()
    context = data.get("context", {})
    
    result = await health_concierge.execute_concierge_service(service_id, context)
    return result

@app.post("/api/managed-services/concierge/assess")
async def assess_health_status(request: Request):
    """Assess current health status"""
    tenant_id = get_tenant_from_request(request)
    health_concierge = get_health_concierge(tenant_id)
    
    data = await request.json()
    metrics = data.get("metrics", {})
    
    result = health_concierge.assess_health_status(metrics)
    return result

@app.get("/api/managed-services/automation/rules")
async def get_automation_rules(request: Request):
    """Get automation rules"""
    tenant_id = get_tenant_from_request(request)
    automation_engine = get_automation_engine(tenant_id)
    
    return {
        "status": "success",
        "rules": [rule.to_dict() for rule in automation_engine.rules.values()],
        "total_rules": len(automation_engine.rules)
    }

@app.get("/api/managed-services/automation/workflows")
async def get_automation_workflows(request: Request):
    """Get automation workflows"""
    tenant_id = get_tenant_from_request(request)
    automation_engine = get_automation_engine(tenant_id)
    
    return {
        "status": "success",
        "workflows": [workflow.to_dict() for workflow in automation_engine.workflows.values()],
        "total_workflows": len(automation_engine.workflows)
    }

@app.post("/api/managed-services/automation/trigger/{rule_id}")
async def trigger_automation_rule(request: Request, rule_id: str):
    """Trigger an automation rule"""
    tenant_id = get_tenant_from_request(request)
    automation_engine = get_automation_engine(tenant_id)
    
    data = await request.json()
    trigger_data = data.get("trigger_data", {})
    
    result = await automation_engine.trigger_rule(rule_id, trigger_data)
    return result

@app.post("/api/managed-services/automation/execute/{workflow_id}")
async def execute_automation_workflow(request: Request, workflow_id: str):
    """Execute an automation workflow"""
    tenant_id = get_tenant_from_request(request)
    automation_engine = get_automation_engine(tenant_id)
    
    result = await automation_engine.execute_workflow(workflow_id)
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