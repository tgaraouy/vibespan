#!/usr/bin/env python3
"""
Setup script for user_001 (first user)
Imports existing health data and creates tenant environment.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.auth.tenant_manager import tenant_manager
from src.data.data_importer import data_importer

def setup_tgaraouy():
    """Set up tgaraouy with existing health data"""
    
    print("🏥 Setting up Vibespan.ai for tgaraouy...")
    
    # User profile data
    user_profile = {
        "name": "Tawfik",
        "email": "tawfik.garaouy@gmail.com",
        "goals": [
            "Optimize health and longevity",
            "Track patterns in health data",
            "Get personalized recommendations",
            "Monitor recovery and performance"
        ],
        "preferences": {
            "timezone": "UTC",
            "units": "metric",
            "notifications": True
        }
    }
    
    # Create tenant
    print("📁 Creating tenant environment...")
    tenant_config = tenant_manager.create_tenant("tgaraouy", user_profile)
    print(f"✅ Tenant created: {tenant_config['tenant_id']}")
    
    # Define data sources (you can add your actual file paths here)
    data_sources = {
        "whoop_data": "../health-agents-system/data/phusio_cycles.csv",
        "food_data": "../health-agents-system/data/food.csv", 
        "supplements_data": "../health-agents-system/data/supplements.csv",
        "workout_data": "../health-agents-system/data/workouts.csv",
        "health_data": "../health-agents-system/data/myhealth_data.csv"
    }
    
    # Import existing data
    print("📊 Importing existing health data...")
    import_results = data_importer.import_user_data("tgaraouy", data_sources)
    
    print(f"✅ Imported {len(import_results['imported_sources'])} data sources")
    print(f"📈 Total records: {import_results['total_records']}")
    
    if import_results['errors']:
        print("⚠️ Errors encountered:")
        for error in import_results['errors']:
            print(f"  - {error}")
    
    # Set up data sources in tenant config
    print("🔗 Configuring data sources...")
    for source in import_results['imported_sources']:
        tenant_manager.add_data_source(
            "tgaraouy",
            source,
            {
                "type": "historical",
                "status": "active",
                "last_updated": "2024-09-23T00:00:00Z"
            }
        )
    
    # Update tenant with active data sources
    tenant_manager.update_tenant("tgaraouy", {
        "data_sources": import_results['imported_sources'],
        "setup_completed": True,
        "setup_date": "2024-09-23T00:00:00Z"
    })
    
    print("🎉 tgaraouy setup complete!")
    print(f"🌐 Access your health agents at: https://tgaraouy.vibespan.ai")
    print(f"📁 Tenant data stored in: tenants/tgaraouy/")
    
    return tenant_config

if __name__ == "__main__":
    setup_tgaraouy()
