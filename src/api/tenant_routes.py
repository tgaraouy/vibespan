#!/usr/bin/env python3
"""
Tenant-specific API routes for Vibespan.ai
Handles subdomain routing and tenant isolation.
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from typing import Dict, Any
import json
from pathlib import Path

from ..auth.tenant_manager import tenant_manager
from .onboarding import router as onboarding_router
from .agent_routes import router as agent_router

router = APIRouter()

# Include sub-routers
router.include_router(onboarding_router, tags=["onboarding"])
router.include_router(agent_router, tags=["agents"])

def get_tenant_id(request: Request) -> str:
    """Extract tenant ID from subdomain"""
    from ..middleware.subdomain_middleware import get_tenant_id_from_request
    return get_tenant_id_from_request(request)

@router.get("/dashboard")
async def tenant_dashboard(request: Request):
    """Tenant dashboard"""
    tenant_id = get_tenant_id(request)
    tenant_config = tenant_manager.get_tenant(tenant_id)
    
    if not tenant_config:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return {
        "tenant_id": tenant_id,
        "subdomain": f"{tenant_id}.vibespan.ai",
        "status": "active",
        "agents": tenant_config.get("active_agents", []),
        "data_sources": tenant_config.get("data_sources", []),
        "created_at": tenant_config.get("created_at")
    }

@router.get("/health")
async def tenant_health(request: Request):
    """Tenant health status"""
    tenant_id = get_tenant_id(request)
    tenant_config = tenant_manager.get_tenant(tenant_id)
    
    if not tenant_config:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return {
        "tenant_id": tenant_id,
        "status": "healthy",
        "agents_active": len(tenant_config.get("active_agents", [])),
        "data_sources": len(tenant_config.get("data_sources", []))
    }

@router.get("/data/summary")
async def data_summary(request: Request):
    """Get summary of tenant's health data"""
    tenant_id = get_tenant_id(request)
    
    # Get data directory
    data_dir = tenant_manager.get_tenant_data_path(tenant_id, "raw")
    
    if not data_dir.exists():
        return {"message": "No data available", "sources": []}
    
    # Scan for data files
    data_files = list(data_dir.glob("*.json"))
    
    summary = {
        "tenant_id": tenant_id,
        "total_files": len(data_files),
        "sources": []
    }
    
    for file_path in data_files:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            
            if isinstance(data, list):
                record_count = len(data)
            else:
                record_count = 1
            
            summary["sources"].append({
                "file": file_path.name,
                "records": record_count,
                "source": data[0].get("source") if isinstance(data, list) else "unknown"
            })
        except Exception as e:
            summary["sources"].append({
                "file": file_path.name,
                "records": 0,
                "error": str(e)
            })
    
    return summary

@router.get("/agents/status")
async def agents_status(request: Request):
    """Get status of tenant's agents"""
    tenant_id = get_tenant_id(request)
    tenant_config = tenant_manager.get_tenant(tenant_id)
    
    if not tenant_config:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return {
        "tenant_id": tenant_id,
        "active_agents": tenant_config.get("active_agents", []),
        "available_tiers": tenant_config.get("agent_tiers", {}),
        "total_agents": len(tenant_config.get("active_agents", []))
    }

@router.post("/agents/activate")
async def activate_agent(request: Request, agent_name: str):
    """Activate a premium agent (upsell)"""
    tenant_id = get_tenant_id(request)
    tenant_config = tenant_manager.get_tenant(tenant_id)
    
    if not tenant_config:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Check if agent is available
    premium_agents = tenant_config.get("agent_tiers", {}).get("premium", [])
    if agent_name not in premium_agents:
        raise HTTPException(status_code=400, detail="Agent not available")
    
    # Add to active agents (in real implementation, this would require payment)
    active_agents = tenant_config.get("active_agents", [])
    if agent_name not in active_agents:
        active_agents.append(agent_name)
        tenant_manager.update_tenant(tenant_id, {"active_agents": active_agents})
        
        # Log audit
        tenant_manager.log_audit(tenant_id, "agent_activated", {"agent": agent_name})
    
    return {
        "message": f"Agent {agent_name} activated",
        "active_agents": active_agents
    }
