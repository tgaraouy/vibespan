#!/usr/bin/env python3
"""
Onboarding API for Vibespan.ai
Handles user onboarding flow with data source selection and agent setup.
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from typing import Dict, Any, List
import json
from pathlib import Path

from ..auth.tenant_manager import tenant_manager
from ..data.data_importer import data_importer

router = APIRouter()

def get_tenant_id(request: Request) -> str:
    """Extract tenant ID from subdomain"""
    from ..middleware.subdomain_middleware import get_tenant_id_from_request
    return get_tenant_id_from_request(request)

@router.get("/onboarding/start")
async def start_onboarding(request: Request):
    """Start the onboarding process"""
    tenant_id = get_tenant_id(request)
    
    # Check if tenant exists
    tenant_config = tenant_manager.get_tenant(tenant_id)
    if not tenant_config:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Check onboarding status
    onboarding_status = tenant_config.get("onboarding_status", "not_started")
    
    return {
        "tenant_id": tenant_id,
        "onboarding_status": onboarding_status,
        "steps": [
            {
                "id": "welcome",
                "title": "Welcome to Vibespan.ai",
                "description": "Your personal health agents are ready to help optimize your wellness journey",
                "completed": onboarding_status != "not_started"
            },
            {
                "id": "data_sources",
                "title": "Connect Your Data Sources",
                "description": "Choose which health data sources you want to connect",
                "completed": len(tenant_config.get("data_sources", [])) > 0
            },
            {
                "id": "goals",
                "title": "Set Your Health Goals",
                "description": "Tell us what you want to achieve with your health",
                "completed": "goals" in tenant_config.get("user_profile", {})
            },
            {
                "id": "agents",
                "title": "Activate Your Agents",
                "description": "Choose which AI agents you want to work with",
                "completed": len(tenant_config.get("active_agents", [])) > 0
            },
            {
                "id": "complete",
                "title": "You're All Set!",
                "description": "Your health agents are ready to start helping you",
                "completed": onboarding_status == "completed"
            }
        ]
    }

@router.get("/onboarding/data-sources")
async def get_available_data_sources(request: Request):
    """Get available data sources for onboarding"""
    return {
        "available_sources": [
            {
                "id": "whoop",
                "name": "WHOOP",
                "description": "Recovery, sleep, and strain data",
                "type": "real_time",
                "icon": "🏃‍♂️",
                "features": ["HRV", "Recovery Score", "Sleep Analysis", "Strain Tracking"]
            },
            {
                "id": "apple_health",
                "name": "Apple Health",
                "description": "Comprehensive health and fitness data",
                "type": "real_time",
                "icon": "🍎",
                "features": ["Heart Rate", "Steps", "Sleep", "Workouts", "Nutrition"]
            },
            {
                "id": "csv_upload",
                "name": "CSV Upload",
                "description": "Upload your historical health data",
                "type": "historical",
                "icon": "📊",
                "features": ["Custom Data", "Historical Analysis", "Pattern Detection"]
            },
            {
                "id": "manual_entry",
                "name": "Manual Entry",
                "description": "Enter health data manually",
                "type": "manual",
                "icon": "✍️",
                "features": ["Custom Tracking", "Personal Notes", "Flexible Input"]
            }
        ]
    }

@router.post("/onboarding/data-sources/connect")
async def connect_data_source(request: Request, source_config: Dict[str, Any]):
    """Connect a data source during onboarding"""
    tenant_id = get_tenant_id(request)
    
    source_id = source_config.get("source_id")
    source_type = source_config.get("type")
    
    if not source_id or not source_type:
        raise HTTPException(status_code=400, detail="Missing source_id or type")
    
    # Add data source to tenant
    success = tenant_manager.add_data_source(
        tenant_id,
        source_id,
        {
            "type": source_type,
            "status": "connected",
            "connected_at": "2024-09-23T00:00:00Z",
            "config": source_config
        }
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to connect data source")
    
    # Update onboarding status
    tenant_config = tenant_manager.get_tenant(tenant_id)
    if tenant_config:
        tenant_manager.update_tenant(tenant_id, {
            "onboarding_status": "data_sources_connected"
        })
    
    return {
        "message": f"Data source {source_id} connected successfully",
        "source_id": source_id,
        "status": "connected"
    }

@router.post("/onboarding/goals")
async def set_health_goals(request: Request, goals: Dict[str, Any]):
    """Set user health goals during onboarding"""
    tenant_id = get_tenant_id(request)
    
    # Update user profile with goals
    tenant_config = tenant_manager.get_tenant(tenant_id)
    if not tenant_config:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    user_profile = tenant_config.get("user_profile", {})
    user_profile["goals"] = goals.get("goals", [])
    user_profile["preferences"] = goals.get("preferences", {})
    
    success = tenant_manager.update_tenant(tenant_id, {
        "user_profile": user_profile,
        "onboarding_status": "goals_set"
    })
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update goals")
    
    return {
        "message": "Health goals set successfully",
        "goals": goals.get("goals", []),
        "preferences": goals.get("preferences", {})
    }

@router.post("/onboarding/agents/activate")
async def activate_agents(request: Request, agent_selection: Dict[str, Any]):
    """Activate agents during onboarding"""
    tenant_id = get_tenant_id(request)
    
    selected_agents = agent_selection.get("agents", [])
    
    # Get tenant config
    tenant_config = tenant_manager.get_tenant(tenant_id)
    if not tenant_config:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Validate selected agents
    available_agents = tenant_config.get("agent_tiers", {}).get("core", [])
    valid_agents = [agent for agent in selected_agents if agent in available_agents]
    
    if not valid_agents:
        raise HTTPException(status_code=400, detail="No valid agents selected")
    
    # Update active agents
    success = tenant_manager.update_tenant(tenant_id, {
        "active_agents": valid_agents,
        "onboarding_status": "agents_activated"
    })
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to activate agents")
    
    return {
        "message": "Agents activated successfully",
        "active_agents": valid_agents,
        "total_agents": len(valid_agents)
    }

@router.post("/onboarding/complete")
async def complete_onboarding(request: Request):
    """Complete the onboarding process"""
    tenant_id = get_tenant_id(request)
    
    # Mark onboarding as completed
    success = tenant_manager.update_tenant(tenant_id, {
        "onboarding_status": "completed",
        "onboarding_completed_at": "2024-09-23T00:00:00Z"
    })
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to complete onboarding")
    
    # Log completion
    tenant_manager.log_audit(tenant_id, "onboarding_completed", {
        "completed_at": "2024-09-23T00:00:00Z"
    })
    
    return {
        "message": "Onboarding completed successfully!",
        "tenant_id": tenant_id,
        "dashboard_url": f"https://{tenant_id}.vibespan.ai/dashboard",
        "status": "completed"
    }
