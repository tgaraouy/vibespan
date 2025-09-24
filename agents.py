#!/usr/bin/env python3
"""
Vibespan.ai Health Agents System
Core AI agents for health data processing and recommendations.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
from virtual_filesystem import get_context_manager

logger = logging.getLogger(__name__)

class HealthAgent:
    """Base class for all health agents"""
    
    def __init__(self, name: str, tenant_id: str):
        self.name = name
        self.tenant_id = tenant_id
        self.logger = logging.getLogger(f"agent.{name}")
        self.context_manager = get_context_manager(tenant_id)
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process health data and return insights"""
        raise NotImplementedError
    
    def _call_llm(self, prompt: str, context: str = "") -> str:
        """Call LLM for enhanced decision making"""
        try:
            # Try OpenAI first
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key:
                try:
                    from openai import OpenAI
                    client = OpenAI(api_key=openai_key)
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": f"You are a health AI agent specialized in {self.name.lower().replace('_', ' ')}. Provide concise, actionable insights."},
                            {"role": "user", "content": f"Context: {context}\n\nPrompt: {prompt}"}
                        ],
                        max_tokens=500,
                        temperature=0.7
                    )
                    return response.choices[0].message.content
                except Exception as e:
                    self.logger.warning(f"OpenAI call failed: {e}")
            
            # Try Anthropic as fallback
            anthropic_key = os.getenv("ANTHROPIC_API_KEY")
            if anthropic_key:
                try:
                    import anthropic
                    client = anthropic.Anthropic(api_key=anthropic_key)
                    response = client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=500,
                        system=f"You are a health AI agent specialized in {self.name.lower().replace('_', ' ')}. Provide concise, actionable insights.",
                        messages=[{"role": "user", "content": f"Context: {context}\n\nPrompt: {prompt}"}]
                    )
                    return response.content[0].text
                except Exception as e:
                    self.logger.warning(f"Anthropic call failed: {e}")
            
            # Fallback to rule-based response
            return self._fallback_response(prompt)
            
        except Exception as e:
            self.logger.error(f"LLM call failed: {e}")
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """Fallback response when LLM is not available"""
        return f"AI analysis unavailable. Using rule-based logic for {self.name}."

class DataCollector(HealthAgent):
    """Collects and normalizes health data from various sources"""
    
    def __init__(self, tenant_id: str):
        super().__init__("DataCollector", tenant_id)
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Collect and normalize health data"""
        self.logger.info(f"Collecting data for tenant {self.tenant_id}")
        
        # Simulate data collection and normalization
        collected_data = {
            "timestamp": datetime.now().isoformat(),
            "sources": data.get("sources", []),
            "records_count": len(data.get("records", [])),
            "data_types": ["heart_rate", "sleep", "recovery", "strain"],
            "status": "collected"
        }
        
        return {
            "agent": self.name,
            "tenant_id": self.tenant_id,
            "result": collected_data,
            "confidence": 0.95
        }

class PatternDetector(HealthAgent):
    """Detects patterns and correlations in health data"""
    
    def __init__(self, tenant_id: str):
        super().__init__("PatternDetector", tenant_id)
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect patterns in health data"""
        self.logger.info(f"Detecting patterns for tenant {self.tenant_id}")
        
        # Save input data to context
        self.context_manager.save_health_data("pattern_analysis", data)
        
        # Get historical context
        recent_insights = self.context_manager.get_recent_insights(5)
        context = f"Recent insights: {len(recent_insights)} patterns found previously"
        
        # Use LLM for enhanced pattern detection
        llm_prompt = f"""
        Analyze this health data for patterns and correlations:
        - Recovery Score: {data.get('recovery_score', 'N/A')}
        - Sleep Duration: {data.get('sleep_duration', 'N/A')} hours
        - Heart Rate Variability: {data.get('heart_rate_variability', 'N/A')}
        - Strain Score: {data.get('strain_score', 'N/A')}
        
        Identify 2-3 key patterns with time delays (0-72 hours) and correlation strength.
        Focus on actionable insights for health optimization.
        """
        
        llm_analysis = self._call_llm(llm_prompt, context)
        
        # Enhanced pattern detection with LLM insights
        patterns = [
            {
                "type": "sleep_recovery_correlation",
                "description": "Sleep quality strongly correlates with recovery score",
                "strength": 0.87,
                "time_delay": "0-24 hours",
                "llm_insight": llm_analysis
            },
            {
                "type": "exercise_hrv_impact",
                "description": "High-intensity exercise affects HRV for 48-72 hours",
                "strength": 0.73,
                "time_delay": "48-72 hours",
                "llm_insight": llm_analysis
            }
        ]
        
        result = {
            "patterns_found": len(patterns),
            "patterns": patterns,
            "confidence": 0.82,
            "llm_enhanced": True,
            "analysis": llm_analysis
        }
        
        # Save pattern insights to context
        self.context_manager.save_pattern_insight(result)
        
        return {
            "agent": self.name,
            "tenant_id": self.tenant_id,
            "result": result
        }

class WorkoutPlanner(HealthAgent):
    """Plans personalized workout recommendations"""
    
    def __init__(self, tenant_id: str):
        super().__init__("WorkoutPlanner", tenant_id)
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate workout recommendations"""
        self.logger.info(f"Planning workouts for tenant {self.tenant_id}")
        
        # Simulate workout planning based on recovery data
        recovery_score = data.get("recovery_score", 75)
        
        if recovery_score >= 80:
            workout_type = "High Intensity"
            duration = "45-60 minutes"
            intensity = "High"
        elif recovery_score >= 60:
            workout_type = "Moderate Intensity"
            duration = "30-45 minutes"
            intensity = "Medium"
        else:
            workout_type = "Recovery"
            duration = "20-30 minutes"
            intensity = "Low"
        
        recommendations = {
            "workout_type": workout_type,
            "duration": duration,
            "intensity": intensity,
            "recovery_based": True,
            "confidence": 0.88
        }
        
        return {
            "agent": self.name,
            "tenant_id": self.tenant_id,
            "result": recommendations
        }

class NutritionPlanner(HealthAgent):
    """Plans personalized nutrition recommendations"""
    
    def __init__(self, tenant_id: str):
        super().__init__("NutritionPlanner", tenant_id)
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate nutrition recommendations"""
        self.logger.info(f"Planning nutrition for tenant {self.tenant_id}")
        
        # Simulate nutrition planning
        recommendations = {
            "hydration": "Drink 2.5-3L water today",
            "macros": "Focus on protein (1.6g/kg body weight)",
            "timing": "Eat within 2 hours post-workout",
            "supplements": ["Magnesium", "Vitamin D", "Omega-3"],
            "confidence": 0.85
        }
        
        return {
            "agent": self.name,
            "tenant_id": self.tenant_id,
            "result": recommendations
        }

class HealthCoach(HealthAgent):
    """Provides personalized health coaching and insights"""
    
    def __init__(self, tenant_id: str):
        super().__init__("HealthCoach", tenant_id)
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate health coaching insights"""
        self.logger.info(f"Coaching insights for tenant {self.tenant_id}")
        
        # Simulate health coaching
        insights = [
            "Your sleep consistency has improved 15% this week",
            "Consider adding 10 minutes of meditation before bed",
            "Your recovery trend is positive - keep up the good work!",
            "Try to maintain your current exercise routine"
        ]
        
        return {
            "agent": self.name,
            "tenant_id": self.tenant_id,
            "result": {
                "insights": insights,
                "mood": "positive",
                "confidence": 0.90
            }
        }

class SafetyOfficer(HealthAgent):
    """Monitors for health safety concerns and alerts"""
    
    def __init__(self, tenant_id: str):
        super().__init__("SafetyOfficer", tenant_id)
    
    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Check for safety concerns"""
        self.logger.info(f"Safety check for tenant {self.tenant_id}")
        
        # Simulate safety monitoring
        alerts = []
        warnings = []
        
        # Check for concerning patterns
        if data.get("recovery_score", 100) < 30:
            alerts.append("Low recovery score detected - consider rest day")
        
        if data.get("sleep_duration", 8) < 6:
            warnings.append("Insufficient sleep duration")
        
        safety_status = {
            "alerts": alerts,
            "warnings": warnings,
            "risk_level": "low" if not alerts else "medium",
            "recommendations": [
                "Monitor recovery metrics closely",
                "Ensure adequate sleep hygiene"
            ]
        }
        
        return {
            "agent": self.name,
            "tenant_id": self.tenant_id,
            "result": safety_status
        }

class AgentOrchestrator:
    """Orchestrates all health agents for a tenant"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.agents = {
            "DataCollector": DataCollector(tenant_id),
            "PatternDetector": PatternDetector(tenant_id),
            "WorkoutPlanner": WorkoutPlanner(tenant_id),
            "NutritionPlanner": NutritionPlanner(tenant_id),
            "HealthCoach": HealthCoach(tenant_id),
            "SafetyOfficer": SafetyOfficer(tenant_id)
        }
        self.logger = logging.getLogger(f"orchestrator.{tenant_id}")
    
    async def process_health_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process health data through all agents"""
        self.logger.info(f"Processing health data for tenant {self.tenant_id}")
        
        results = {}
        agent_results = []
        
        # Process through each agent
        for agent_name, agent in self.agents.items():
            try:
                result = await agent.process(data)
                results[agent_name] = result
                agent_results.append({
                    "agent": agent_name,
                    "status": "success",
                    "confidence": result.get("confidence", 0.0)
                })
            except Exception as e:
                self.logger.error(f"Agent {agent_name} failed: {e}")
                agent_results.append({
                    "agent": agent_name,
                    "status": "error",
                    "error": str(e)
                })
        
        # Generate summary
        summary = {
            "tenant_id": self.tenant_id,
            "timestamp": datetime.now().isoformat(),
            "agents_processed": len(agent_results),
            "successful_agents": len([r for r in agent_results if r["status"] == "success"]),
            "agent_results": agent_results,
            "overall_confidence": sum([r.get("confidence", 0) for r in agent_results if r["status"] == "success"]) / max(1, len([r for r in agent_results if r["status"] == "success"]))
        }
        
        return {
            "summary": summary,
            "agent_results": results
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            "tenant_id": self.tenant_id,
            "total_agents": len(self.agents),
            "available_agents": list(self.agents.keys()),
            "status": "operational"
        }

# Global agent orchestrators for each tenant
_agent_orchestrators: Dict[str, AgentOrchestrator] = {}

def get_agent_orchestrator(tenant_id: str) -> AgentOrchestrator:
    """Get or create agent orchestrator for tenant"""
    if tenant_id not in _agent_orchestrators:
        _agent_orchestrators[tenant_id] = AgentOrchestrator(tenant_id)
    return _agent_orchestrators[tenant_id]
