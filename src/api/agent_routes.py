#!/usr/bin/env python3
"""
Agent API Routes for Vibespan.ai
Handles agent interactions and health data processing.
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from typing import Dict, Any, List
import json

from ..agents.agent_orchestrator import get_orchestrator
from ..auth.tenant_manager import tenant_manager

router = APIRouter()

def get_tenant_id(request: Request) -> str:
    """Extract tenant ID from subdomain"""
    from ..middleware.subdomain_middleware import get_tenant_id_from_request
    return get_tenant_id_from_request(request)

@router.get("/agents/status")
async def get_agents_status(request: Request):
    """Get status of all agents for the tenant"""
    tenant_id = get_tenant_id(request)
    
    orchestrator = get_orchestrator(tenant_id)
    status = orchestrator.get_agent_status()
    
    return status

@router.post("/agents/process")
async def process_health_data(request: Request, data: Dict[str, Any]):
    """Process health data through all active agents"""
    tenant_id = get_tenant_id(request)
    
    # Validate tenant exists
    tenant_config = tenant_manager.get_tenant(tenant_id)
    if not tenant_config:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Get orchestrator and process data
    orchestrator = get_orchestrator(tenant_id)
    results = orchestrator.process_health_data(data)
    
    return results

@router.get("/agents/insights")
async def get_insights(request: Request):
    """Get recent insights from agents"""
    tenant_id = get_tenant_id(request)
    
    orchestrator = get_orchestrator(tenant_id)
    insights = orchestrator.get_insights_summary()
    
    return insights

@router.post("/agents/activate")
async def activate_agent(request: Request, agent_config: Dict[str, Any]):
    """Activate a new agent"""
    tenant_id = get_tenant_id(request)
    agent_type = agent_config.get("agent_type")
    
    if not agent_type:
        raise HTTPException(status_code=400, detail="Missing agent_type")
    
    # Check if agent is available for this tenant
    tenant_config = tenant_manager.get_tenant(tenant_id)
    if not tenant_config:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    available_agents = tenant_config.get("agent_tiers", {}).get("core", [])
    if agent_type not in available_agents:
        raise HTTPException(status_code=400, detail=f"Agent {agent_type} not available")
    
    # Activate agent
    orchestrator = get_orchestrator(tenant_id)
    success = orchestrator.activate_agent(agent_type)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to activate agent")
    
    return {
        "message": f"Agent {agent_type} activated successfully",
        "agent_type": agent_type,
        "status": "active"
    }

@router.post("/agents/deactivate")
async def deactivate_agent(request: Request, agent_config: Dict[str, Any]):
    """Deactivate an agent"""
    tenant_id = get_tenant_id(request)
    agent_type = agent_config.get("agent_type")
    
    if not agent_type:
        raise HTTPException(status_code=400, detail="Missing agent_type")
    
    # Deactivate agent
    orchestrator = get_orchestrator(tenant_id)
    success = orchestrator.deactivate_agent(agent_type)
    
    if not success:
        raise HTTPException(status_code=400, detail="Agent not found or already inactive")
    
    return {
        "message": f"Agent {agent_type} deactivated successfully",
        "agent_type": agent_type,
        "status": "inactive"
    }

@router.get("/agents/available")
async def get_available_agents(request: Request):
    """Get available agents for the tenant"""
    tenant_id = get_tenant_id(request)
    
    tenant_config = tenant_manager.get_tenant(tenant_id)
    if not tenant_config:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    agent_tiers = tenant_config.get("agent_tiers", {})
    active_agents = tenant_config.get("active_agents", [])
    
    # Format available agents
    available = []
    for tier, agents in agent_tiers.items():
        for agent in agents:
            available.append({
                "agent_type": agent,
                "tier": tier,
                "active": agent in active_agents,
                "description": _get_agent_description(agent)
            })
    
    return {
        "available_agents": available,
        "total_available": len(available),
        "active_count": len(active_agents)
    }

def _get_agent_description(agent_type: str) -> str:
    """Get description for an agent type"""
    descriptions = {
        "DataCollector": "Collects and normalizes health data from various sources",
        "PatternDetector": "Detects patterns and correlations in your health data",
        "BasicWorkoutPlanner": "Provides personalized workout recommendations",
        "BasicNutritionPlanner": "Offers nutrition guidance based on your health data",
        "HealthCoach": "Provides general health coaching and motivation",
        "SafetyOfficer": "Monitors your health data for safety concerns and alerts"
    }
    
    return descriptions.get(agent_type, "Health optimization agent")

@router.post("/agents/chat")
async def chat_with_agents(request: Request, chat_data: Dict[str, Any]):
    """Chat with agents for health questions"""
    tenant_id = get_tenant_id(request)
    user_message = chat_data.get("message", "")
    
    if not user_message:
        raise HTTPException(status_code=400, detail="Missing message")
    
    # Get orchestrator
    orchestrator = get_orchestrator(tenant_id)
    
    # Simulate agent chat response
    response = {
        "tenant_id": tenant_id,
        "user_message": user_message,
        "agent_response": f"Hello! I'm your health AI assistant. I've analyzed your message: '{user_message}'. Based on your health data, I can help you with workout planning, nutrition advice, and health insights. What would you like to know more about?",
        "suggested_actions": [
            "Get workout recommendation",
            "Check nutrition advice",
            "View health insights",
            "Set health goals"
        ],
        "timestamp": "2024-09-23T00:00:00Z"
    }
    
    return response
