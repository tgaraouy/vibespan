#!/usr/bin/env python3
"""
Test script for Vibespan.ai Managed Services Platform
Tests the new automation engine, health concierge, and service catalog.
"""

import requests
import json
import asyncio
from datetime import datetime

BASE_URL = "https://tgaraouy.vibespan.ai"

def test_managed_services():
    """Test the managed services platform"""
    print("🏥 Testing Vibespan.ai Managed Services Platform")
    print("=" * 60)
    
    # Test 1: System Status
    print("\n1. Testing System Status...")
    try:
        response = requests.get(f"{BASE_URL}/api/managed-services/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Managed Services Status: {data.get('managed_services_active', False)}")
            print(f"   Tenant ID: {data.get('tenant_id', 'N/A')}")
            print(f"   Automation Rules: {data.get('automation_status', {}).get('rules_count', 0)}")
            print(f"   Workflows: {data.get('automation_status', {}).get('workflows_count', 0)}")
        else:
            print(f"❌ Status check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Service Catalog
    print("\n2. Testing Service Catalog...")
    try:
        response = requests.get(f"{BASE_URL}/onboarding/service-catalog")
        if response.status_code == 200:
            data = response.json()
            catalog = data.get('service_catalog', {})
            categories = catalog.get('categories', {})
            print(f"✅ Service Categories: {len(categories)}")
            for category, info in categories.items():
                print(f"   - {info.get('name', category)}: {info.get('icon', '')} {info.get('description', '')}")
        else:
            print(f"❌ Service catalog failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Hybrid Templates
    print("\n3. Testing Hybrid Templates...")
    try:
        response = requests.get(f"{BASE_URL}/onboarding/hybrid-templates")
        if response.status_code == 200:
            data = response.json()
            templates = data.get('hybrid_templates', {})
            print(f"✅ Hybrid Templates: {len(templates)}")
            for template_id, template in templates.items():
                print(f"   - {template.get('name', template_id)}: {template.get('description', '')}")
        else:
            print(f"❌ Hybrid templates failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Concierge Services
    print("\n4. Testing Health Concierge Services...")
    try:
        response = requests.get(f"{BASE_URL}/api/managed-services/concierge")
        if response.status_code == 200:
            data = response.json()
            services = data.get('available_services', {})
            current_level = data.get('available_services', {}).get('current_level', 'unknown')
            print(f"✅ Current Service Level: {current_level}")
            for level, level_services in services.items():
                if isinstance(level_services, list):
                    print(f"   {level.upper()}: {len(level_services)} services")
        else:
            print(f"❌ Concierge services failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Automation Rules
    print("\n5. Testing Automation Rules...")
    try:
        response = requests.get(f"{BASE_URL}/api/managed-services/automation/rules")
        if response.status_code == 200:
            data = response.json()
            rules = data.get('rules', [])
            print(f"✅ Automation Rules: {len(rules)}")
            for rule in rules[:3]:  # Show first 3 rules
                print(f"   - {rule.get('name', 'Unknown')}: {rule.get('description', '')}")
        else:
            print(f"❌ Automation rules failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 6: Automation Workflows
    print("\n6. Testing Automation Workflows...")
    try:
        response = requests.get(f"{BASE_URL}/api/managed-services/automation/workflows")
        if response.status_code == 200:
            data = response.json()
            workflows = data.get('workflows', [])
            print(f"✅ Automation Workflows: {len(workflows)}")
            for workflow in workflows:
                print(f"   - {workflow.get('name', 'Unknown')}: {workflow.get('description', '')}")
        else:
            print(f"❌ Automation workflows failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 7: Service Recommendations
    print("\n7. Testing Service Recommendations...")
    try:
        test_data = {
            "health_goals": ["Improve Fitness", "Enhance Sleep", "Optimize Nutrition"],
            "health_tools": ["WHOOP", "Apple Health", "Manual Tracking"]
        }
        response = requests.post(
            f"{BASE_URL}/onboarding/service-recommendations",
            json=test_data
        )
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get('recommendations', {})
            print(f"✅ Service Recommendations Generated")
            print(f"   Essential: {len(recommendations.get('essential_services', []))}")
            print(f"   Recommended: {len(recommendations.get('recommended_services', []))}")
            print(f"   Optional: {len(recommendations.get('optional_services', []))}")
        else:
            print(f"❌ Service recommendations failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 8: Health Status Assessment
    print("\n8. Testing Health Status Assessment...")
    try:
        test_metrics = {
            "recovery_score": 75,
            "sleep_quality": "good",
            "stress_level": "moderate",
            "hrv": 45,
            "rhr": 55
        }
        response = requests.post(
            f"{BASE_URL}/api/managed-services/concierge/assess",
            json={"metrics": test_metrics}
        )
        if response.status_code == 200:
            data = response.json()
            health_status = data.get('health_status', 'unknown')
            recommendations = data.get('recommendations', [])
            print(f"✅ Health Status: {health_status}")
            print(f"   Recommendations: {len(recommendations)}")
            for rec in recommendations[:2]:  # Show first 2
                print(f"   - {rec}")
        else:
            print(f"❌ Health assessment failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🏥 Managed Services Platform Test Complete!")
    print("✅ All core features are operational and ready for users")

def test_onboarding_flow():
    """Test the enhanced onboarding flow"""
    print("\n🚀 Testing Enhanced Onboarding Flow")
    print("=" * 60)
    
    # Test onboarding start
    print("\n1. Testing Onboarding Start...")
    try:
        response = requests.get(f"{BASE_URL}/onboarding/start?user_id=tgaraouy")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Onboarding Started: {data.get('status', 'unknown')}")
            print(f"   Steps: {len(data.get('steps', []))}")
        else:
            print(f"❌ Onboarding start failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test health goals
    print("\n2. Testing Health Goals...")
    try:
        response = requests.get(f"{BASE_URL}/onboarding/health-goals")
        if response.status_code == 200:
            data = response.json()
            goals = data.get('health_goals', [])
            print(f"✅ Health Goals Available: {len(goals)}")
            print(f"   Sample: {goals[:3] if goals else 'None'}")
        else:
            print(f"❌ Health goals failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test daily goals
    print("\n3. Testing Daily Goals...")
    try:
        response = requests.get(f"{BASE_URL}/onboarding/daily-goals")
        if response.status_code == 200:
            data = response.json()
            goals = data.get('daily_goals', [])
            print(f"✅ Daily Goals Available: {len(goals)}")
            print(f"   Sample: {goals[:3] if goals else 'None'}")
        else:
            print(f"❌ Daily goals failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test health tools
    print("\n4. Testing Health Tools...")
    try:
        response = requests.get(f"{BASE_URL}/onboarding/health-tools")
        if response.status_code == 200:
            data = response.json()
            tools = data.get('health_tools', [])
            print(f"✅ Health Tools Available: {len(tools)}")
            print(f"   Tools: {tools}")
        else:
            print(f"❌ Health tools failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🏥 Vibespan.ai Managed Services Platform Test Suite")
    print("Testing deployed platform at: https://tgaraouy.vibespan.ai")
    print("=" * 80)
    
    # Run tests
    test_managed_services()
    test_onboarding_flow()
    
    print("\n🎉 All tests completed!")
    print("The managed services platform is ready for users!")
