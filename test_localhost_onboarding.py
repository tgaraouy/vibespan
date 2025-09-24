#!/usr/bin/env python3
"""
Test Localhost Onboarding for Vibespan.ai
Tests the complete onboarding flow using tgaraouy.localhost:8000
"""

import requests
import json
import time

BASE_URL = "http://tgaraouy.localhost:8000"

def test_onboarding_flow():
    """Test the complete onboarding flow"""
    
    print("🏥 Testing Vibespan.ai Onboarding Flow")
    print("=" * 50)
    print(f"🌐 Using: {BASE_URL}")
    print()
    
    # Step 1: Start onboarding
    print("1️⃣ Starting onboarding process...")
    try:
        response = requests.get(f"{BASE_URL}/onboarding/start")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Onboarding started")
            print(f"   - Tenant ID: {data['tenant_id']}")
            print(f"   - Status: {data['onboarding_status']}")
            print(f"   - Steps: {len(data['steps'])}")
            
            # Show onboarding steps
            for i, step in enumerate(data['steps'], 1):
                status = "✅" if step['completed'] else "⏳"
                print(f"   {i}. {status} {step['title']}")
        else:
            print(f"❌ Failed to start onboarding: {response.status_code}")
            print(f"   Error: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - is the server running?")
        print("   Try: python main.py")
        return
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return
    
    # Step 2: Get available data sources
    print("\n2️⃣ Getting available data sources...")
    try:
        response = requests.get(f"{BASE_URL}/onboarding/data-sources")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {len(data['available_sources'])} data sources:")
            for source in data['available_sources']:
                print(f"   - {source['icon']} {source['name']}: {source['description']}")
        else:
            print(f"❌ Failed to get data sources: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Step 3: Connect a data source
    print("\n3️⃣ Connecting WHOOP data source...")
    try:
        whoop_config = {
            "source_id": "whoop",
            "type": "real_time",
            "config": {
                "webhook_url": f"{BASE_URL}/webhook/whoop/tgaraouy",
                "scopes": ["read:recovery", "read:cycles", "read:sleep", "read:workout"]
            }
        }
        
        response = requests.post(f"{BASE_URL}/onboarding/data-sources/connect", json=whoop_config)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ WHOOP connected successfully")
            print(f"   - Source: {data['source_id']}")
            print(f"   - Status: {data['status']}")
        else:
            print(f"❌ Failed to connect WHOOP: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Step 4: Set health goals
    print("\n4️⃣ Setting health goals...")
    try:
        goals_data = {
            "goals": [
                "performance",
                "recovery",
                "longevity"
            ],
            "preferences": {
                "workout_frequency": "5-6 times per week",
                "diet_preference": "balanced",
                "sleep_target": "8 hours",
                "focus_areas": ["HRV optimization", "Sleep quality", "Recovery"]
            }
        }
        
        response = requests.post(f"{BASE_URL}/onboarding/goals", json=goals_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health goals set successfully")
            print(f"   - Goals: {', '.join(data['goals'])}")
            print(f"   - Preferences: {len(data['preferences'])} items")
        else:
            print(f"❌ Failed to set goals: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Step 5: Activate agents
    print("\n5️⃣ Activating health agents...")
    try:
        agent_selection = {
            "agents": [
                "DataCollector",
                "PatternDetector", 
                "BasicWorkoutPlanner",
                "BasicNutritionPlanner",
                "HealthCoach",
                "SafetyOfficer"
            ]
        }
        
        response = requests.post(f"{BASE_URL}/onboarding/agents/activate", json=agent_selection)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agents activated successfully")
            print(f"   - Active agents: {data['total_agents']}")
            print(f"   - Agents: {', '.join(data['active_agents'])}")
        else:
            print(f"❌ Failed to activate agents: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Step 6: Complete onboarding
    print("\n6️⃣ Completing onboarding...")
    try:
        response = requests.post(f"{BASE_URL}/onboarding/complete")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Onboarding completed successfully!")
            print(f"   - Status: {data['status']}")
            print(f"   - Dashboard: {data['dashboard_url']}")
        else:
            print(f"❌ Failed to complete onboarding: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Step 7: Test dashboard access
    print("\n7️⃣ Testing dashboard access...")
    try:
        response = requests.get(f"{BASE_URL}/dashboard")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Dashboard accessible")
            print(f"   - Tenant: {data['tenant_id']}")
            print(f"   - Subdomain: {data['subdomain']}")
            print(f"   - Status: {data['status']}")
            print(f"   - Active agents: {len(data['agents'])}")
            print(f"   - Data sources: {len(data['data_sources'])}")
        else:
            print(f"❌ Dashboard not accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Step 8: Test agent status
    print("\n8️⃣ Testing agent status...")
    try:
        response = requests.get(f"{BASE_URL}/agents/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent status retrieved")
            print(f"   - Total agents: {data['total_agents']}")
            print(f"   - Active agents: {list(data['agents'].keys())}")
        else:
            print(f"❌ Failed to get agent status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Onboarding Flow Test Complete!")
    print(f"🌐 Your health agents are ready at: {BASE_URL}")
    print("📊 You can now access your personalized health dashboard")
    print("🤖 All AI agents are active and ready to help optimize your wellness")

if __name__ == "__main__":
    test_onboarding_flow()
