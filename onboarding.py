#!/usr/bin/env python3
"""
Comprehensive Onboarding System for Vibespan.ai
Guides users through health goal setting and container provisioning.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from user_containers import container_manager, HEALTH_TEMPLATES
from service_catalog import service_catalog

logger = logging.getLogger(__name__)

class OnboardingFlow:
    """Manages the user onboarding process"""
    
    def __init__(self):
        self.steps = [
            "welcome",
            "health_goals", 
            "daily_goals",
            "health_tools",
            "service_configuration",
            "data_preferences",
            "template_selection",
            "container_provisioning",
            "dashboard_setup"
        ]
        self.logger = logging.getLogger("onboarding")
    
    def start_onboarding(self, user_id: str) -> Dict[str, Any]:
        """Start the onboarding process for a new user"""
        return {
            "status": "onboarding_started",
            "user_id": user_id,
            "current_step": "welcome",
            "total_steps": len(self.steps),
            "steps": self.steps,
            "welcome_message": f"Welcome to Vibespan.ai, {user_id}! Let's set up your personalized health journey.",
            "next_action": "Set your health goals"
        }
    
    def get_health_goals_options(self) -> List[Dict[str, Any]]:
        """Get available health goals for user selection"""
        return [
            {
                "id": "improve_fitness",
                "title": "Improve Fitness",
                "description": "Build strength, endurance, and overall fitness",
                "category": "fitness",
                "icon": "💪"
            },
            {
                "id": "better_sleep",
                "title": "Better Sleep",
                "description": "Optimize sleep quality and duration",
                "category": "recovery",
                "icon": "😴"
            },
            {
                "id": "reduce_stress",
                "title": "Reduce Stress",
                "description": "Manage stress levels and improve mental health",
                "category": "wellness",
                "icon": "🧘"
            },
            {
                "id": "improve_nutrition",
                "title": "Improve Nutrition",
                "description": "Optimize diet and eating habits",
                "category": "nutrition",
                "icon": "🥗"
            },
            {
                "id": "increase_energy",
                "title": "Increase Energy",
                "description": "Boost daily energy levels and vitality",
                "category": "wellness",
                "icon": "⚡"
            },
            {
                "id": "weight_management",
                "title": "Weight Management",
                "description": "Achieve and maintain healthy weight",
                "category": "fitness",
                "icon": "⚖️"
            },
            {
                "id": "longevity",
                "title": "Longevity",
                "description": "Optimize health for long-term wellness",
                "category": "optimization",
                "icon": "🌱"
            },
            {
                "id": "peak_performance",
                "title": "Peak Performance",
                "description": "Achieve optimal physical and mental performance",
                "category": "optimization",
                "icon": "🏆"
            }
        ]
    
    def get_daily_goals_options(self) -> List[Dict[str, Any]]:
        """Get available daily goals for user selection"""
        return [
            {
                "id": "consistent_sleep",
                "title": "Consistent Sleep Schedule",
                "description": "Go to bed and wake up at the same time daily",
                "category": "sleep",
                "frequency": "daily"
            },
            {
                "id": "daily_movement",
                "title": "Daily Movement",
                "description": "Get at least 30 minutes of physical activity",
                "category": "exercise",
                "frequency": "daily"
            },
            {
                "id": "hydration_goal",
                "title": "Hydration Goal",
                "description": "Drink 8+ glasses of water daily",
                "category": "nutrition",
                "frequency": "daily"
            },
            {
                "id": "stress_management",
                "title": "Stress Management",
                "description": "Practice 10+ minutes of stress relief daily",
                "category": "wellness",
                "frequency": "daily"
            },
            {
                "id": "nutrition_tracking",
                "title": "Nutrition Tracking",
                "description": "Log meals and track nutrition intake",
                "category": "nutrition",
                "frequency": "daily"
            },
            {
                "id": "recovery_focus",
                "title": "Recovery Focus",
                "description": "Prioritize recovery and rest",
                "category": "recovery",
                "frequency": "daily"
            }
        ]
    
    def get_health_tools_options(self) -> List[Dict[str, Any]]:
        """Get available health tools and devices"""
        return [
            {
                "id": "whoop",
                "name": "WHOOP",
                "description": "Recovery, sleep, and strain tracking",
                "type": "wearable",
                "features": ["recovery_score", "hrv", "sleep_analysis", "strain_tracking"],
                "integration": "webhook"
            },
            {
                "id": "apple_health",
                "name": "Apple Health",
                "description": "iPhone and Apple Watch health data",
                "type": "mobile",
                "features": ["steps", "heart_rate", "sleep", "activity"],
                "integration": "api"
            },
            {
                "id": "fitbit",
                "name": "Fitbit",
                "description": "Activity and sleep tracking",
                "type": "wearable",
                "features": ["steps", "sleep_score", "active_minutes", "heart_rate"],
                "integration": "api"
            },
            {
                "id": "garmin",
                "name": "Garmin",
                "description": "Fitness and sports tracking",
                "type": "wearable",
                "features": ["gps_tracking", "heart_rate", "sleep", "stress"],
                "integration": "api"
            },
            {
                "id": "oura",
                "name": "Oura Ring",
                "description": "Sleep and recovery optimization",
                "type": "wearable",
                "features": ["sleep_score", "recovery_index", "activity_score"],
                "integration": "api"
            },
            {
                "id": "manual_tracking",
                "name": "Manual Tracking",
                "description": "Log data manually through our interface",
                "type": "manual",
                "features": ["custom_metrics", "flexible_logging", "personal_notes"],
                "integration": "ui"
            }
        ]
    
    def get_health_templates(self) -> Dict[str, Any]:
        """Get available health templates"""
        return HEALTH_TEMPLATES
    
    def get_service_catalog(self) -> Dict[str, Any]:
        """Get comprehensive service catalog"""
        return service_catalog.get_all_services()
    
    def get_hybrid_templates(self) -> Dict[str, Any]:
        """Get hybrid template combinations"""
        return service_catalog.get_hybrid_templates()
    
    def get_service_recommendations(self, health_goals: List[str], health_tools: List[str]) -> Dict[str, Any]:
        """Get service recommendations based on user goals and tools"""
        recommendations = {
            "essential_services": [],
            "recommended_services": [],
            "optional_services": []
        }
        
        # Essential services for everyone
        recommendations["essential_services"] = [
            "recovery_tracking",
            "health_coaching", 
            "safety_monitoring"
        ]
        
        # Recommendations based on goals
        if any("fitness" in goal.lower() for goal in health_goals):
            recommendations["recommended_services"].extend([
                "workout_planning",
                "strength_tracking",
                "performance_optimization"
            ])
        
        if any("sleep" in goal.lower() or "recovery" in goal.lower() for goal in health_goals):
            recommendations["recommended_services"].extend([
                "sleep_optimization",
                "stress_management"
            ])
        
        if any("nutrition" in goal.lower() for goal in health_goals):
            recommendations["recommended_services"].extend([
                "nutrition_planning",
                "hydration_tracking"
            ])
        
        if any("longevity" in goal.lower() for goal in health_goals):
            recommendations["recommended_services"].extend([
                "longevity_tracking",
                "biomarker_monitoring",
                "lifestyle_optimization"
            ])
        
        # Optional services based on tools
        if len(health_tools) > 1:
            recommendations["optional_services"].extend([
                "pattern_detection",
                "predictive_analytics",
                "health_insights"
            ])
        
        return recommendations
    
    def process_onboarding_step(self, user_id: str, step: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a specific onboarding step"""
        if step == "health_goals":
            return self._process_health_goals(user_id, data)
        elif step == "daily_goals":
            return self._process_daily_goals(user_id, data)
        elif step == "health_tools":
            return self._process_health_tools(user_id, data)
        elif step == "service_configuration":
            return self._process_service_configuration(user_id, data)
        elif step == "template_selection":
            return self._process_template_selection(user_id, data)
        elif step == "container_provisioning":
            return self._process_container_provisioning(user_id, data)
        else:
            return {
                "status": "step_processed",
                "step": step,
                "data": data,
                "next_step": self._get_next_step(step)
            }
    
    def _process_health_goals(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process health goals selection"""
        selected_goals = data.get("selected_goals", [])
        
        return {
            "status": "health_goals_selected",
            "user_id": user_id,
            "selected_goals": selected_goals,
            "goals_count": len(selected_goals),
            "next_step": "daily_goals",
            "message": f"Great! You've selected {len(selected_goals)} health goals. Now let's set your daily habits."
        }
    
    def _process_daily_goals(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process daily goals selection"""
        selected_daily_goals = data.get("selected_daily_goals", [])
        
        return {
            "status": "daily_goals_selected",
            "user_id": user_id,
            "selected_daily_goals": selected_daily_goals,
            "daily_goals_count": len(selected_daily_goals),
            "next_step": "health_tools",
            "message": f"Excellent! {len(selected_daily_goals)} daily habits selected. Now let's connect your health tools."
        }
    
    def _process_health_tools(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process health tools selection"""
        selected_tools = data.get("selected_tools", [])
        
        return {
            "status": "health_tools_selected",
            "user_id": user_id,
            "selected_tools": selected_tools,
            "tools_count": len(selected_tools),
            "next_step": "service_configuration",
            "message": f"Perfect! {len(selected_tools)} health tools selected. Now let's configure your services."
        }
    
    def _process_service_configuration(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process service configuration step"""
        service_config = data.get("service_configuration", {})
        hybrid_template = data.get("hybrid_template")
        
        # If hybrid template is selected, apply it
        if hybrid_template:
            hybrid_templates = service_catalog.get_hybrid_templates()
            if hybrid_template in hybrid_templates:
                template_config = hybrid_templates[hybrid_template]["services"]
                for service_id, priority in template_config.items():
                    service_config[service_id] = {
                        "enabled": priority != "disabled",
                        "priority": priority,
                        "custom_config": {}
                    }
        
        return {
            "status": "service_configuration_processed",
            "user_id": user_id,
            "service_configuration": service_config,
            "hybrid_template": hybrid_template,
            "next_step": "template_selection",
            "message": "Services configured. Now let's choose your health template."
        }
    
    def _process_template_selection(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process health template selection"""
        selected_template = data.get("selected_template", "wellness_focused")
        
        return {
            "status": "template_selected",
            "user_id": user_id,
            "selected_template": selected_template,
            "template_info": HEALTH_TEMPLATES.get(selected_template, {}),
            "next_step": "container_provisioning",
            "message": "Template selected! Now let's create your personalized health container."
        }
    
    def _process_container_provisioning(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process container provisioning"""
        # Combine all onboarding data
        onboarding_data = {
            "name": data.get("name", user_id),
            "email": data.get("email", f"{user_id}@vibespan.ai"),
            "health_goals": data.get("health_goals", []),
            "daily_goals": data.get("daily_goals", []),
            "health_tools": data.get("health_tools", []),
            "data_sources": data.get("health_tools", []),  # Same as health_tools
            "preferences": {
                "data_sharing": data.get("data_sharing", "private"),
                "notifications": data.get("notifications", True),
                "units": data.get("units", "metric"),
                "timezone": data.get("timezone", "UTC")
            },
            "template": data.get("selected_template", "wellness_focused")
        }
        
        # Provision the container
        result = container_manager.provision_container(user_id, onboarding_data)
        
        if result["status"] == "provisioned":
            return {
                "status": "onboarding_completed",
                "user_id": user_id,
                "container": result["container"],
                "dashboard_url": result["container"]["dashboard_url"],
                "message": f"Welcome to your personalized health journey, {user_id}!",
                "next_steps": result["next_steps"]
            }
        else:
            return {
                "status": "provisioning_failed",
                "user_id": user_id,
                "error": result.get("error", "Unknown error"),
                "message": "Failed to create your health container. Please try again."
            }
    
    def _get_next_step(self, current_step: str) -> Optional[str]:
        """Get the next step in the onboarding flow"""
        try:
            current_index = self.steps.index(current_step)
            if current_index < len(self.steps) - 1:
                return self.steps[current_index + 1]
        except ValueError:
            pass
        return None
    
    def complete_onboarding(self, user_id: str) -> Dict[str, Any]:
        """Complete the onboarding process"""
        container = container_manager.get_container(user_id)
        if not container:
            return {
                "status": "error",
                "message": "Container not found. Please restart onboarding."
            }
        
        return {
            "status": "onboarding_completed",
            "user_id": user_id,
            "container_info": container.get_container_info(),
            "dashboard_url": container.get_container_info()["dashboard_url"],
            "message": f"Onboarding completed! Your personalized health container is ready.",
            "welcome_message": f"Welcome to Vibespan.ai, {user_id}! Your health journey starts now."
        }

# Global onboarding flow
onboarding_flow = OnboardingFlow()
