#!/usr/bin/env python3
"""
User Container System for Vibespan.ai
Each user gets their own isolated container with personalized health setup.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import hashlib
import secrets

logger = logging.getLogger(__name__)

class UserContainer:
    """Represents a user's isolated health container"""
    
    def __init__(self, user_id: str, user_profile: Dict[str, Any]):
        self.user_id = user_id
        self.subdomain = user_id  # Use user_id as subdomain
        self.profile = user_profile
        self.container_id = self._generate_container_id()
        self.created_at = datetime.now()
        self.status = "active"
        self.logger = logging.getLogger(f"container.{user_id}")
        
        # Container configuration
        self.health_goals = user_profile.get("health_goals", [])
        self.daily_goals = user_profile.get("daily_goals", [])
        self.health_tools = user_profile.get("health_tools", [])
        self.data_sources = user_profile.get("data_sources", [])
        self.preferences = user_profile.get("preferences", {})
        
        # Container state
        self.agents_enabled = self._determine_agents()
        self.templates_loaded = self._load_health_templates()
        self.data_collection_active = True
        
    def _generate_container_id(self) -> str:
        """Generate unique container ID"""
        return hashlib.md5(f"{self.user_id}_{self.created_at.isoformat()}".encode()).hexdigest()[:12]
    
    def _determine_agents(self) -> List[str]:
        """Determine which agents to enable based on user profile"""
        base_agents = ["DataCollector", "SafetyOfficer"]
        
        # Add agents based on health goals
        if any("fitness" in goal.lower() or "exercise" in goal.lower() for goal in self.health_goals):
            base_agents.extend(["WorkoutPlanner", "PatternDetector"])
        
        if any("nutrition" in goal.lower() or "diet" in goal.lower() for goal in self.health_goals):
            base_agents.append("NutritionPlanner")
        
        if any("sleep" in goal.lower() or "recovery" in goal.lower() for goal in self.health_goals):
            base_agents.extend(["PatternDetector", "HealthCoach"])
        
        # Always add HealthCoach for personalized insights
        if "HealthCoach" not in base_agents:
            base_agents.append("HealthCoach")
        
        return list(set(base_agents))  # Remove duplicates
    
    def _load_health_templates(self) -> Dict[str, Any]:
        """Load health data collection templates based on user profile"""
        templates = {
            "basic_metrics": {
                "name": "Basic Health Metrics",
                "description": "Essential health tracking",
                "fields": ["sleep_duration", "energy_level", "mood", "stress_level"],
                "frequency": "daily"
            }
        }
        
        # Add templates based on health tools
        if "whoop" in self.health_tools:
            templates["whoop_metrics"] = {
                "name": "WHOOP Recovery & Sleep",
                "description": "WHOOP device metrics",
                "fields": ["recovery_score", "hrv", "sleep_duration", "sleep_efficiency", "strain_score"],
                "frequency": "real-time",
                "webhook_enabled": True
            }
        
        if "apple_health" in self.health_tools:
            templates["apple_health"] = {
                "name": "Apple Health Integration",
                "description": "iPhone/Apple Watch data",
                "fields": ["steps", "heart_rate", "active_energy", "exercise_minutes"],
                "frequency": "daily"
            }
        
        if "fitbit" in self.health_tools:
            templates["fitbit_metrics"] = {
                "name": "Fitbit Activity & Sleep",
                "description": "Fitbit device data",
                "fields": ["steps", "floors", "active_minutes", "sleep_score"],
                "frequency": "daily"
            }
        
        # Add nutrition template if nutrition is a goal
        if any("nutrition" in goal.lower() for goal in self.health_goals):
            templates["nutrition_tracking"] = {
                "name": "Nutrition & Hydration",
                "description": "Food and water intake tracking",
                "fields": ["water_intake", "meals_logged", "supplements_taken", "hunger_level"],
                "frequency": "daily"
            }
        
        # Add exercise template if fitness is a goal
        if any("fitness" in goal.lower() for goal in self.health_goals):
            templates["exercise_tracking"] = {
                "name": "Exercise & Activity",
                "description": "Workout and activity tracking",
                "fields": ["workout_type", "duration", "intensity", "perceived_exertion"],
                "frequency": "per_workout"
            }
        
        return templates
    
    def get_container_info(self) -> Dict[str, Any]:
        """Get complete container information"""
        return {
            "container_id": self.container_id,
            "user_id": self.user_id,
            "subdomain": self.subdomain,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "health_goals": self.health_goals,
            "daily_goals": self.daily_goals,
            "health_tools": self.health_tools,
            "data_sources": self.data_sources,
            "preferences": self.preferences,
            "agents_enabled": self.agents_enabled,
            "templates_loaded": list(self.templates_loaded.keys()),
            "data_collection_active": self.data_collection_active,
            "dashboard_url": f"https://{self.subdomain}.vibespan.ai/dashboard"
        }
    
    def update_goals(self, new_goals: Dict[str, Any]) -> Dict[str, Any]:
        """Update user goals and reconfigure container"""
        if "health_goals" in new_goals:
            self.health_goals = new_goals["health_goals"]
            self.agents_enabled = self._determine_agents()
        
        if "daily_goals" in new_goals:
            self.daily_goals = new_goals["daily_goals"]
        
        if "health_tools" in new_goals:
            self.health_tools = new_goals["health_tools"]
            self.templates_loaded = self._load_health_templates()
        
        return {
            "status": "updated",
            "container_id": self.container_id,
            "updated_at": datetime.now().isoformat(),
            "changes": list(new_goals.keys())
        }
    
    def get_daily_actions(self) -> List[Dict[str, Any]]:
        """Generate personalized daily actions based on goals and tools"""
        actions = []
        
        # Base actions for all users
        actions.extend([
            {
                "id": "check_energy",
                "title": "Check Energy Level",
                "description": "Rate your energy level (1-10)",
                "category": "basic_metrics",
                "priority": "high",
                "template": "basic_metrics"
            },
            {
                "id": "check_mood",
                "title": "Check Mood",
                "description": "Rate your mood (1-10)",
                "category": "basic_metrics", 
                "priority": "high",
                "template": "basic_metrics"
            }
        ])
        
        # WHOOP-specific actions
        if "whoop" in self.health_tools:
            actions.extend([
                {
                    "id": "check_recovery",
                    "title": "Check WHOOP Recovery",
                    "description": "Review your recovery score and HRV",
                    "category": "recovery",
                    "priority": "high",
                    "template": "whoop_metrics"
                },
                {
                    "id": "review_sleep",
                    "title": "Review Sleep Quality",
                    "description": "Analyze last night's sleep data",
                    "category": "sleep",
                    "priority": "high",
                    "template": "whoop_metrics"
                }
            ])
        
        # Fitness-related actions
        if any("fitness" in goal.lower() for goal in self.health_goals):
            actions.extend([
                {
                    "id": "plan_workout",
                    "title": "Plan Today's Workout",
                    "description": "Based on recovery, plan your training",
                    "category": "exercise",
                    "priority": "medium",
                    "template": "exercise_tracking"
                },
                {
                    "id": "log_activity",
                    "title": "Log Physical Activity",
                    "description": "Record any exercise or movement",
                    "category": "exercise",
                    "priority": "medium",
                    "template": "exercise_tracking"
                }
            ])
        
        # Nutrition-related actions
        if any("nutrition" in goal.lower() for goal in self.health_goals):
            actions.extend([
                {
                    "id": "hydration_check",
                    "title": "Hydration Check",
                    "description": "Track your water intake",
                    "category": "nutrition",
                    "priority": "medium",
                    "template": "nutrition_tracking"
                },
                {
                    "id": "meal_planning",
                    "title": "Meal Planning",
                    "description": "Plan your meals for the day",
                    "category": "nutrition",
                    "priority": "medium",
                    "template": "nutrition_tracking"
                }
            ])
        
        return actions

class ContainerManager:
    """Manages user containers and provisioning"""
    
    def __init__(self):
        self.containers: Dict[str, UserContainer] = {}
        self.logger = logging.getLogger("container_manager")
    
    def create_container(self, user_id: str, user_profile: Dict[str, Any]) -> UserContainer:
        """Create a new user container"""
        if user_id in self.containers:
            raise ValueError(f"Container for user {user_id} already exists")
        
        container = UserContainer(user_id, user_profile)
        self.containers[user_id] = container
        
        self.logger.info(f"Created container {container.container_id} for user {user_id}")
        return container
    
    def get_container(self, user_id: str) -> Optional[UserContainer]:
        """Get user container by ID"""
        return self.containers.get(user_id)
    
    def list_containers(self) -> List[Dict[str, Any]]:
        """List all containers"""
        return [container.get_container_info() for container in self.containers.values()]
    
    def provision_container(self, user_id: str, onboarding_data: Dict[str, Any]) -> Dict[str, Any]:
        """Provision a new container with onboarding data"""
        try:
            # Create container
            container = self.create_container(user_id, onboarding_data)
            
            # Initialize container resources
            container_info = container.get_container_info()
            
            return {
                "status": "provisioned",
                "container": container_info,
                "next_steps": [
                    "Container created successfully",
                    f"Access your dashboard at: {container_info['dashboard_url']}",
                    "Your health agents are now active",
                    "Data collection templates are loaded",
                    "Start tracking your health metrics"
                ],
                "provisioned_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Container provisioning failed for {user_id}: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "user_id": user_id
            }

# Health templates for different user types
HEALTH_TEMPLATES = {
    "fitness_enthusiast": {
        "name": "Fitness Enthusiast",
        "description": "For users focused on fitness and performance",
        "default_goals": ["improve_fitness", "increase_strength", "better_recovery"],
        "default_tools": ["whoop", "apple_health"],
        "default_actions": ["workout_planning", "recovery_tracking", "performance_monitoring"]
    },
    "wellness_focused": {
        "name": "Wellness Focused",
        "description": "For users focused on overall wellness and balance",
        "default_goals": ["better_sleep", "reduce_stress", "improve_nutrition"],
        "default_tools": ["apple_health", "fitbit"],
        "default_actions": ["sleep_tracking", "stress_monitoring", "nutrition_logging"]
    },
    "health_optimizer": {
        "name": "Health Optimizer",
        "description": "For users wanting comprehensive health optimization",
        "default_goals": ["longevity", "peak_performance", "optimal_health"],
        "default_tools": ["whoop", "apple_health", "fitbit"],
        "default_actions": ["comprehensive_tracking", "pattern_analysis", "optimization_recommendations"]
    }
}

# Global container manager
container_manager = ContainerManager()
