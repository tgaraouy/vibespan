#!/usr/bin/env python3
"""
Test tgaraouy Onboarding for Vibespan.ai
Tests the complete onboarding flow using Host header to simulate tgaraouy.vibespan.ai
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"
HEADERS = {"Host": "tgaraouy.vibespan.ai"}

def test_onboarding_flow():
    """Test the complete onboarding flow"""
    
    print("🏥 Testing Vibespan.ai Onboarding Flow for tgaraouy")
    print("=" * 60)
    print(f"🌐 Using: {BASE_URL} with Host: {HEADERS['Host']}")
    print()
    
    # Step 1: Start onboarding
    print("1️⃣ Starting onboarding process...")
    try:
        response = requests.get(f"{BASE_URL}/onboarding/start", headers=HEADERS)
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
        response = requests.get(f"{BASE_URL}/onboarding/data-sources", headers=HEADERS)
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
                "webhook_url": f"https://tgaraouy.vibespan.ai/webhook/whoop/tgaraouy",
                "scopes": ["read:recovery", "read:cycles", "read:sleep", "read:workout"]
            }
        }
        
        response = requests.post(f"{BASE_URL}/onboarding/data-sources/connect", 
                               json=whoop_config, headers=HEADERS)
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
        
        response = requests.post(f"{BASE_URL}/onboarding/goals", 
                               json=goals_data, headers=HEADERS)
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
        
        response = requests.post(f"{BASE_URL}/onboarding/agents/activate", 
                               json=agent_selection, headers=HEADERS)
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
        response = requests.post(f"{BASE_URL}/onboarding/complete", headers=HEADERS)
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
        response = requests.get(f"{BASE_URL}/dashboard", headers=HEADERS)
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
        response = requests.get(f"{BASE_URL}/agents/status", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent status retrieved")
            print(f"   - Total agents: {data['total_agents']}")
            print(f"   - Active agents: {list(data['agents'].keys())}")
        else:
            print(f"❌ Failed to get agent status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Step 9: Test agent processing
    print("\n9️⃣ Testing agent processing...")
    try:
        sample_health_data = {
            "recovery_score": 78,
            "sleep_quality": 8.2,
            "hrv": 47,
            "heart_rate_resting": 62,
            "goals": ["performance", "recovery"],
            "recent_trends": {
                "sleep_improvement": True,
                "hrv_decline": False
            }
        }
        
        response = requests.post(f"{BASE_URL}/agents/process", 
                               json=sample_health_data, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent processing successful")
            print(f"   - Agents processed: {len(data['agents_processed'])}")
            print(f"   - Insights generated: {len(data['insights'])}")
            print(f"   - Recommendations: {len(data['recommendations'])}")
            
            # Show sample insights
            if data['insights']:
                print(f"   - Sample insights:")
                for insight in data['insights'][:3]:
                    print(f"     • {insight}")
        else:
            print(f"❌ Failed to process with agents: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎉 Onboarding Flow Test Complete!")
    print(f"🌐 Your health agents are ready at: https://tgaraouy.vibespan.ai")
    print("📊 You can now access your personalized health dashboard")
    print("🤖 All AI agents are active and ready to help optimize your wellness")
    print("\n💡 To test in browser:")
    print("   - Use a tool like Postman or curl with Host header")
    print("   - Or modify your browser's developer tools to add the Host header")

if __name__ == "__main__":
    test_onboarding_flow()
