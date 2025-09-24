#!/usr/bin/env python3
"""
Agent Orchestrator for Vibespan.ai
Coordinates multiple agents and manages their communication.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from .core_agents import create_agent, BaseAgent
from ..auth.tenant_manager import tenant_manager

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """Orchestrates multiple health agents for a tenant"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.agents: Dict[str, BaseAgent] = {}
        self.logger = logging.getLogger(f"AgentOrchestrator_{tenant_id}")
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize agents for this tenant"""
        tenant_config = tenant_manager.get_tenant(self.tenant_id)
        if not tenant_config:
            self.logger.error(f"Tenant {self.tenant_id} not found")
            return
        
        active_agents = tenant_config.get("active_agents", [])
        
        for agent_type in active_agents:
            try:
                agent = create_agent(agent_type, self.tenant_id)
                self.agents[agent_type] = agent
                self.logger.info(f"Initialized agent: {agent_type}")
            except Exception as e:
                self.logger.error(f"Failed to initialize agent {agent_type}: {str(e)}")
    
    def process_health_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process health data through all active agents"""
        self.logger.info(f"Processing health data for tenant {self.tenant_id}")
        
        results = {
            "tenant_id": self.tenant_id,
            "timestamp": datetime.utcnow().isoformat(),
            "agents_processed": [],
            "insights": [],
            "recommendations": [],
            "alerts": [],
            "warnings": []
        }
        
        # Process through each agent
        for agent_type, agent in self.agents.items():
            try:
                agent_result = agent.process(data)
                results["agents_processed"].append(agent_type)
                
                # Extract insights
                if "insights" in agent_result:
                    results["insights"].extend(agent_result["insights"])
                
                # Extract recommendations
                if agent_type in ["BasicWorkoutPlanner", "BasicNutritionPlanner"]:
                    if "result" in agent_result:
                        results["recommendations"].append({
                            "agent": agent_type,
                            "recommendation": agent_result["result"]
                        })
                
                # Extract alerts and warnings
                if agent_type == "SafetyOfficer":
                    if "result" in agent_result:
                        safety_result = agent_result["result"]
                        if "alerts" in safety_result:
                            results["alerts"].extend(safety_result["alerts"])
                        if "warnings" in safety_result:
                            results["warnings"].extend(safety_result["warnings"])
                
                self.logger.info(f"Agent {agent_type} processed successfully")
                
            except Exception as e:
                self.logger.error(f"Agent {agent_type} failed: {str(e)}")
                results["agents_processed"].append(f"{agent_type}_error")
        
        # Store results
        self._store_results(results)
        
        return results
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {
            "tenant_id": self.tenant_id,
            "total_agents": len(self.agents),
            "agents": {}
        }
        
        for agent_type, agent in self.agents.items():
            status["agents"][agent_type] = agent.get_status()
        
        return status
    
    def activate_agent(self, agent_type: str) -> bool:
        """Activate a new agent"""
        try:
            agent = create_agent(agent_type, self.tenant_id)
            self.agents[agent_type] = agent
            
            # Update tenant config
            tenant_config = tenant_manager.get_tenant(self.tenant_id)
            if tenant_config:
                active_agents = tenant_config.get("active_agents", [])
                if agent_type not in active_agents:
                    active_agents.append(agent_type)
                    tenant_manager.update_tenant(self.tenant_id, {
                        "active_agents": active_agents
                    })
            
            self.logger.info(f"Activated agent: {agent_type}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to activate agent {agent_type}: {str(e)}")
            return False
    
    def deactivate_agent(self, agent_type: str) -> bool:
        """Deactivate an agent"""
        if agent_type in self.agents:
            del self.agents[agent_type]
            
            # Update tenant config
            tenant_config = tenant_manager.get_tenant(self.tenant_id)
            if tenant_config:
                active_agents = tenant_config.get("active_agents", [])
                if agent_type in active_agents:
                    active_agents.remove(agent_type)
                    tenant_manager.update_tenant(self.tenant_id, {
                        "active_agents": active_agents
                    })
            
            self.logger.info(f"Deactivated agent: {agent_type}")
            return True
        
        return False
    
    def _store_results(self, results: Dict[str, Any]):
        """Store agent processing results"""
        try:
            # Get tenant data directory
            data_dir = tenant_manager.get_tenant_data_path(self.tenant_id, "derived")
            
            # Create results file
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            results_file = data_dir / f"agent_results_{timestamp}.json"
            
            with open(results_file, "w") as f:
                json.dump(results, f, indent=2)
            
            # Log audit
            tenant_manager.log_audit(self.tenant_id, "agent_processing", {
                "agents_processed": len(results["agents_processed"]),
                "insights_generated": len(results["insights"]),
                "recommendations_generated": len(results["recommendations"]),
                "results_file": str(results_file)
            })
            
        except Exception as e:
            self.logger.error(f"Failed to store results: {str(e)}")
    
    def get_insights_summary(self) -> Dict[str, Any]:
        """Get a summary of recent insights"""
        try:
            # Get recent results files
            data_dir = tenant_manager.get_tenant_data_path(self.tenant_id, "derived")
            results_files = list(data_dir.glob("agent_results_*.json"))
            
            if not results_files:
                return {"message": "No insights available yet"}
            
            # Get the most recent file
            latest_file = max(results_files, key=lambda x: x.stat().st_mtime)
            
            with open(latest_file, "r") as f:
                latest_results = json.load(f)
            
            return {
                "latest_insights": latest_results.get("insights", []),
                "recommendations": latest_results.get("recommendations", []),
                "alerts": latest_results.get("alerts", []),
                "warnings": latest_results.get("warnings", []),
                "timestamp": latest_results.get("timestamp"),
                "agents_used": latest_results.get("agents_processed", [])
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get insights summary: {str(e)}")
            return {"error": str(e)}

# Global orchestrator instances
_orchestrators: Dict[str, AgentOrchestrator] = {}

def get_orchestrator(tenant_id: str) -> AgentOrchestrator:
    """Get or create orchestrator for tenant"""
    if tenant_id not in _orchestrators:
        _orchestrators[tenant_id] = AgentOrchestrator(tenant_id)
    
    return _orchestrators[tenant_id]
