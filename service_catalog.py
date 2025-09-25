#!/usr/bin/env python3
"""
Comprehensive Service Catalog for Vibespan.ai
All available health services with granular control and priority settings.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class HealthService:
    """Represents a health service with configuration options"""
    
    def __init__(self, service_id: str, name: str, description: str, category: str, 
                 priority_levels: List[str], dependencies: List[str] = None):
        self.service_id = service_id
        self.name = name
        self.description = description
        self.category = category
        self.priority_levels = priority_levels  # ["high", "medium", "low", "disabled"]
        self.dependencies = dependencies or []
        self.enabled = True
        self.priority = "medium"
        self.custom_config = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "service_id": self.service_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "priority_levels": self.priority_levels,
            "dependencies": self.dependencies,
            "enabled": self.enabled,
            "priority": self.priority,
            "custom_config": self.custom_config
        }

class ServiceCatalog:
    """Comprehensive catalog of all available health services"""
    
    def __init__(self):
        self.services = self._initialize_services()
        self.categories = self._get_categories()
    
    def _initialize_services(self) -> Dict[str, HealthService]:
        """Initialize all available health services"""
        services = {}
        
        # FITNESS & PERFORMANCE SERVICES
        services["workout_planning"] = HealthService(
            "workout_planning",
            "Fitness Planning",
            "AI-powered fitness planning based on recovery and wellness goals",
            "fitness",
            ["high", "medium", "low", "disabled"],
            ["recovery_tracking", "pattern_detection"]
        )
        
        services["strength_tracking"] = HealthService(
            "strength_tracking",
            "Strength Progress Tracking",
            "Track strength gains and progressive overload",
            "fitness",
            ["high", "medium", "low", "disabled"],
            ["workout_planning"]
        )
        
        services["performance_optimization"] = HealthService(
            "performance_optimization",
            "Fitness Performance Optimization",
            "Optimize fitness training for peak wellness performance",
            "fitness",
            ["high", "medium", "low", "disabled"],
            ["recovery_tracking", "workout_planning", "pattern_detection"]
        )
        
        # RECOVERY & SLEEP SERVICES
        services["recovery_tracking"] = HealthService(
            "recovery_tracking",
            "Wellness Recovery Tracking",
            "Monitor wellness recovery metrics and readiness",
            "recovery",
            ["high", "medium", "low", "disabled"],
            []
        )
        
        services["sleep_optimization"] = HealthService(
            "sleep_optimization",
            "Sleep Optimization",
            "Optimize sleep quality and duration",
            "recovery",
            ["high", "medium", "low", "disabled"],
            ["recovery_tracking"]
        )
        
        services["stress_management"] = HealthService(
            "stress_management",
            "Stress Management",
            "Monitor and manage stress levels",
            "recovery",
            ["high", "medium", "low", "disabled"],
            ["recovery_tracking"]
        )
        
        # NUTRITION & WELLNESS SERVICES
        services["nutrition_planning"] = HealthService(
            "nutrition_planning",
            "Nutrition Planning",
            "Personalized nutrition and meal planning",
            "nutrition",
            ["high", "medium", "low", "disabled"],
            []
        )
        
        services["hydration_tracking"] = HealthService(
            "hydration_tracking",
            "Hydration Tracking",
            "Monitor and optimize hydration levels",
            "nutrition",
            ["high", "medium", "low", "disabled"],
            []
        )
        
        services["supplement_optimization"] = HealthService(
            "supplement_optimization",
            "Supplement Optimization",
            "Optimize supplement timing and dosages",
            "nutrition",
            ["high", "medium", "low", "disabled"],
            ["nutrition_planning", "recovery_tracking"]
        )
        
        # LONGEVITY & OPTIMIZATION SERVICES
        services["longevity_tracking"] = HealthService(
            "longevity_tracking",
            "Longevity Tracking",
            "Track biomarkers and longevity metrics",
            "longevity",
            ["high", "medium", "low", "disabled"],
            ["recovery_tracking", "nutrition_planning"]
        )
        
        services["biomarker_monitoring"] = HealthService(
            "biomarker_monitoring",
            "Biomarker Monitoring",
            "Monitor key health biomarkers",
            "longevity",
            ["high", "medium", "low", "disabled"],
            ["pattern_detection"]
        )
        
        services["lifestyle_optimization"] = HealthService(
            "lifestyle_optimization",
            "Lifestyle Optimization",
            "Optimize daily habits and routines",
            "longevity",
            ["high", "medium", "low", "disabled"],
            ["pattern_detection", "recovery_tracking"]
        )
        
        # DATA & ANALYTICS SERVICES
        services["pattern_detection"] = HealthService(
            "pattern_detection",
            "Pattern Detection",
            "AI-powered pattern recognition in health data",
            "analytics",
            ["high", "medium", "low", "disabled"],
            []
        )
        
        services["predictive_analytics"] = HealthService(
            "predictive_analytics",
            "Predictive Analytics",
            "Predict health trends and outcomes",
            "analytics",
            ["high", "medium", "low", "disabled"],
            ["pattern_detection"]
        )
        
        services["health_insights"] = HealthService(
            "health_insights",
            "Health Insights",
            "Generate personalized health insights",
            "analytics",
            ["high", "medium", "low", "disabled"],
            ["pattern_detection", "recovery_tracking"]
        )
        
        # COACHING & GUIDANCE SERVICES
        services["health_coaching"] = HealthService(
            "health_coaching",
            "Health Coaching",
            "Personalized health coaching and guidance",
            "coaching",
            ["high", "medium", "low", "disabled"],
            ["health_insights"]
        )
        
        services["goal_tracking"] = HealthService(
            "goal_tracking",
            "Goal Tracking",
            "Track progress toward health goals",
            "coaching",
            ["high", "medium", "low", "disabled"],
            []
        )
        
        services["habit_formation"] = HealthService(
            "habit_formation",
            "Habit Formation",
            "Build and maintain healthy habits",
            "coaching",
            ["high", "medium", "low", "disabled"],
            ["goal_tracking"]
        )
        
        # SAFETY & MONITORING SERVICES
        services["safety_monitoring"] = HealthService(
            "safety_monitoring",
            "Safety Monitoring",
            "Monitor for health safety concerns",
            "safety",
            ["high", "medium", "low", "disabled"],
            ["recovery_tracking"]
        )
        
        services["alert_system"] = HealthService(
            "alert_system",
            "Alert System",
            "Health alerts and notifications",
            "safety",
            ["high", "medium", "low", "disabled"],
            ["safety_monitoring"]
        )
        
        return services
    
    def _get_categories(self) -> Dict[str, Dict[str, Any]]:
        """Get service categories with descriptions"""
        return {
            "fitness": {
                "name": "Fitness & Performance",
                "description": "Workout planning, strength tracking, performance optimization",
                "icon": "💪",
                "color": "#e74c3c"
            },
            "recovery": {
                "name": "Recovery & Sleep",
                "description": "Recovery tracking, sleep optimization, stress management",
                "icon": "😴",
                "color": "#3498db"
            },
            "nutrition": {
                "name": "Nutrition & Wellness",
                "description": "Nutrition planning, hydration, supplement optimization",
                "icon": "🥗",
                "color": "#2ecc71"
            },
            "longevity": {
                "name": "Longevity & Optimization",
                "description": "Longevity tracking, biomarker monitoring, lifestyle optimization",
                "icon": "🌱",
                "color": "#9b59b6"
            },
            "analytics": {
                "name": "Data & Analytics",
                "description": "Pattern detection, predictive analytics, health insights",
                "icon": "📊",
                "color": "#f39c12"
            },
            "coaching": {
                "name": "Coaching & Guidance",
                "description": "Health coaching, goal tracking, habit formation",
                "icon": "🎯",
                "color": "#1abc9c"
            },
            "safety": {
                "name": "Safety & Monitoring",
                "description": "Safety monitoring, alerts, health protection",
                "icon": "🛡️",
                "color": "#e67e22"
            }
        }
    
    def get_all_services(self) -> Dict[str, Any]:
        """Get all services organized by category"""
        result = {
            "categories": self.categories,
            "services": {}
        }
        
        for category in self.categories.keys():
            result["services"][category] = [
                service.to_dict() for service in self.services.values()
                if service.category == category
            ]
        
        return result
    
    def get_service(self, service_id: str) -> Optional[HealthService]:
        """Get a specific service by ID"""
        return self.services.get(service_id)
    
    def get_services_by_category(self, category: str) -> List[HealthService]:
        """Get all services in a specific category"""
        return [service for service in self.services.values() if service.category == category]
    
    def get_hybrid_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get hybrid template combinations"""
        return {
            "fitness_wellness_hybrid": {
                "name": "Fitness + Wellness Hybrid",
                "description": "Combine fitness performance with wellness balance",
                "services": {
                    "workout_planning": "high",
                    "recovery_tracking": "high",
                    "sleep_optimization": "high",
                    "nutrition_planning": "medium",
                    "stress_management": "medium",
                    "health_coaching": "high"
                }
            },
            "performance_longevity_hybrid": {
                "name": "Performance + Longevity Hybrid",
                "description": "Peak performance with longevity optimization",
                "services": {
                    "performance_optimization": "high",
                    "longevity_tracking": "high",
                    "biomarker_monitoring": "high",
                    "recovery_tracking": "high",
                    "supplement_optimization": "medium",
                    "lifestyle_optimization": "high"
                }
            },
            "wellness_longevity_hybrid": {
                "name": "Wellness + Longevity Hybrid",
                "description": "Holistic wellness with longevity focus",
                "services": {
                    "sleep_optimization": "high",
                    "stress_management": "high",
                    "nutrition_planning": "high",
                    "longevity_tracking": "high",
                    "lifestyle_optimization": "high",
                    "habit_formation": "medium"
                }
            },
            "comprehensive_optimizer": {
                "name": "Comprehensive Optimizer",
                "description": "All services enabled with balanced priorities",
                "services": {
                    "workout_planning": "medium",
                    "recovery_tracking": "high",
                    "sleep_optimization": "high",
                    "nutrition_planning": "medium",
                    "stress_management": "medium",
                    "longevity_tracking": "medium",
                    "pattern_detection": "high",
                    "health_coaching": "high",
                    "safety_monitoring": "high"
                }
            },
            "minimal_essential": {
                "name": "Minimal Essential",
                "description": "Core services only for simplicity",
                "services": {
                    "recovery_tracking": "high",
                    "health_coaching": "medium",
                    "safety_monitoring": "high"
                }
            }
        }
    
    def create_custom_configuration(self, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Create custom service configuration based on user preferences"""
        config = {}
        
        for service_id, service in self.services.items():
            if service_id in user_preferences:
                config[service_id] = {
                    "enabled": user_preferences[service_id].get("enabled", True),
                    "priority": user_preferences[service_id].get("priority", "medium"),
                    "custom_config": user_preferences[service_id].get("custom_config", {})
                }
            else:
                config[service_id] = {
                    "enabled": False,
                    "priority": "disabled",
                    "custom_config": {}
                }
        
        return config

# Global service catalog
service_catalog = ServiceCatalog()
