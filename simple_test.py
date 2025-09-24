#!/usr/bin/env python3
"""
Simple Test for Vibespan.ai
Tests the basic functionality without complex subdomain routing.
"""

import requests
import json

def test_basic_functionality():
    """Test basic functionality"""
    
    print("🧪 Testing Vibespan.ai Basic Functionality")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Root endpoint
    print("1️⃣ Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Dashboard with Host header
    print("\n2️⃣ Testing dashboard with Host header...")
    try:
        headers = {"Host": "tgaraouy.localhost:8000"}
        response = requests.get(f"{base_url}/dashboard", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Dashboard working for tenant: {data['tenant_id']}")
            print(f"   - Status: {data['status']}")
            print(f"   - Agents: {len(data['agents'])}")
        else:
            print(f"❌ Dashboard failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Agent status
    print("\n3️⃣ Testing agent status...")
    try:
        headers = {"Host": "tgaraouy.localhost:8000"}
        response = requests.get(f"{base_url}/agents/status", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent status working")
            print(f"   - Total agents: {data['total_agents']}")
            print(f"   - Active agents: {list(data['agents'].keys())}")
        else:
            print(f"❌ Agent status failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Agent processing
    print("\n4️⃣ Testing agent processing...")
    try:
        headers = {"Host": "tgaraouy.localhost:8000"}
        sample_data = {
            "recovery_score": 75,
            "sleep_quality": 7.5,
            "hrv": 45,
            "goals": ["performance", "recovery"]
        }
        response = requests.post(f"{base_url}/agents/process", 
                               json=sample_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Agent processing working")
            print(f"   - Agents processed: {len(data['agents_processed'])}")
            print(f"   - Insights: {len(data['insights'])}")
            print(f"   - Recommendations: {len(data['recommendations'])}")
        else:
            print(f"❌ Agent processing failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Basic functionality test complete!")

if __name__ == "__main__":
    test_basic_functionality()
