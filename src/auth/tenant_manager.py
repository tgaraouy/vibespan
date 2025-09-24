#!/usr/bin/env python3
"""
Tenant Manager for Vibespan.ai
Handles tenant creation, isolation, and data management.
"""

import os
import json
import uuid
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
# from cryptography.fernet import Fernet  # Will add later

class TenantManager:
    def __init__(self, base_dir: Path = Path("tenants")):
        self.base_dir = base_dir
        self.base_dir.mkdir(exist_ok=True)
    
    def create_tenant(self, user_id: str, user_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new tenant with isolated environment"""
        
        # Create tenant directory structure
        tenant_dir = self.base_dir / user_id
        tenant_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (tenant_dir / "data" / "phi").mkdir(parents=True, exist_ok=True)
        (tenant_dir / "data" / "derived").mkdir(parents=True, exist_ok=True)
        (tenant_dir / "data" / "raw").mkdir(parents=True, exist_ok=True)
        (tenant_dir / "agents" / "core").mkdir(parents=True, exist_ok=True)
        (tenant_dir / "agents" / "premium").mkdir(parents=True, exist_ok=True)
        (tenant_dir / "config").mkdir(parents=True, exist_ok=True)
        (tenant_dir / "audit").mkdir(parents=True, exist_ok=True)
        
        # Generate encryption key for this tenant (placeholder for now)
        encryption_key = "placeholder_encryption_key_32_bytes_long"
        
        # Create tenant configuration
        tenant_config = {
            "tenant_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "encryption_key": encryption_key,
            "data_retention_days": 1095,  # 3 years
            "agent_tiers": {
                "core": ["DataCollector", "PatternDetector", "BasicWorkoutPlanner", "BasicNutritionPlanner", "HealthCoach", "SafetyOfficer"],
                "premium": ["AdvancedWorkoutPlanner", "PersonalizedNutritionist", "MedicationSpecialist", "SleepOptimizer", "StressManager", "PerformanceAnalyst", "LongevityCoach"]
            },
            "active_agents": ["DataCollector", "PatternDetector", "BasicWorkoutPlanner", "BasicNutritionPlanner", "HealthCoach", "SafetyOfficer"],
            "data_sources": [],
            "user_profile": user_data or {}
        }
        
        # Save tenant configuration
        config_path = tenant_dir / "config" / "tenant.json"
        with open(config_path, "w") as f:
            json.dump(tenant_config, f, indent=2)
        
        # Create audit log
        audit_log = {
            "tenant_id": user_id,
            "action": "tenant_created",
            "timestamp": datetime.utcnow().isoformat(),
            "details": {"user_data_keys": list(user_data.keys()) if user_data else []}
        }
        
        audit_path = tenant_dir / "audit" / f"audit_{datetime.utcnow().strftime('%Y%m%d')}.jsonl"
        with open(audit_path, "a") as f:
            f.write(json.dumps(audit_log) + "\n")
        
        return tenant_config
    
    def get_tenant(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get tenant configuration"""
        tenant_dir = self.base_dir / user_id
        config_path = tenant_dir / "config" / "tenant.json"
        
        if not config_path.exists():
            return None
        
        with open(config_path, "r") as f:
            return json.load(f)
    
    def update_tenant(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update tenant configuration"""
        tenant_config = self.get_tenant(user_id)
        if not tenant_config:
            return False
        
        tenant_config.update(updates)
        tenant_config["updated_at"] = datetime.utcnow().isoformat()
        
        tenant_dir = self.base_dir / user_id
        config_path = tenant_dir / "config" / "tenant.json"
        
        with open(config_path, "w") as f:
            json.dump(tenant_config, f, indent=2)
        
        return True
    
    def add_data_source(self, user_id: str, source_type: str, source_config: Dict[str, Any]) -> bool:
        """Add a data source to tenant"""
        tenant_config = self.get_tenant(user_id)
        if not tenant_config:
            return False
        
        source_id = str(uuid.uuid4())
        source_data = {
            "source_id": source_id,
            "source_type": source_type,
            "config": source_config,
            "added_at": datetime.utcnow().isoformat(),
            "status": "active"
        }
        
        tenant_config["data_sources"].append(source_data)
        return self.update_tenant(user_id, {"data_sources": tenant_config["data_sources"]})
    
    def get_tenant_data_path(self, user_id: str, data_type: str) -> Path:
        """Get path for tenant data"""
        return self.base_dir / user_id / "data" / data_type
    
    def log_audit(self, user_id: str, action: str, details: Dict[str, Any]) -> None:
        """Log audit event for tenant"""
        audit_log = {
            "tenant_id": user_id,
            "action": action,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details
        }
        
        tenant_dir = self.base_dir / user_id
        audit_path = tenant_dir / "audit" / f"audit_{datetime.utcnow().strftime('%Y%m%d')}.jsonl"
        with open(audit_path, "a") as f:
            f.write(json.dumps(audit_log) + "\n")

# Global tenant manager instance
tenant_manager = TenantManager()
