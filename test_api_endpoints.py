#!/usr/bin/env python3
"""
Test API Endpoints for Vibespan.ai
Tests all the API endpoints locally.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, headers=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            print(f"❌ Unsupported method: {method}")
            return None
        
        print(f"{method.upper()} {endpoint}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success: {json.dumps(result, indent=2)[:200]}...")
        else:
            print(f"   ❌ Error: {response.text}")
        
        return response
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection failed - is the server running on {BASE_URL}?")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def main():
    """Test all API endpoints"""
    print("🧪 Testing Vibespan.ai API Endpoints")
    print("=" * 50)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    # Test root endpoint
    print("\n1️⃣ Testing root endpoint...")
    test_endpoint("GET", "/")
    
    # Test tenant dashboard (simulate tgaraouy subdomain)
    print("\n2️⃣ Testing tenant dashboard...")
    headers = {"Host": "tgaraouy.vibespan.ai"}
    test_endpoint("GET", "/dashboard", headers=headers)
    
    # Test tenant health
    print("\n3️⃣ Testing tenant health...")
    test_endpoint("GET", "/health", headers=headers)
    
    # Test data summary
    print("\n4️⃣ Testing data summary...")
    test_endpoint("GET", "/data/summary", headers=headers)
    
    # Test agent status
    print("\n5️⃣ Testing agent status...")
    test_endpoint("GET", "/agents/status", headers=headers)
    
    # Test available agents
    print("\n6️⃣ Testing available agents...")
    test_endpoint("GET", "/agents/available", headers=headers)
    
    # Test agent processing
    print("\n7️⃣ Testing agent processing...")
    sample_data = {
        "recovery_score": 80,
        "sleep_quality": 8.0,
        "hrv": 50,
        "goals": ["performance", "recovery"]
    }
    test_endpoint("POST", "/agents/process", data=sample_data, headers=headers)
    
    # Test agent chat
    print("\n8️⃣ Testing agent chat...")
    chat_data = {"message": "What workout should I do today?"}
    test_endpoint("POST", "/agents/chat", data=chat_data, headers=headers)
    
    # Test onboarding start
    print("\n9️⃣ Testing onboarding...")
    test_endpoint("GET", "/onboarding/start", headers=headers)
    
    # Test available data sources
    print("\n🔟 Testing data sources...")
    test_endpoint("GET", "/onboarding/data-sources", headers=headers)
    
    # Test webhook status
    print("\n1️⃣1️⃣ Testing webhook status...")
    test_endpoint("GET", "/webhook/status/tgaraouy")
    
    # Test webhook test endpoint
    print("\n1️⃣2️⃣ Testing webhook test...")
    test_webhook_data = {
        "test_metric": 75,
        "timestamp": "2024-09-23T12:00:00Z"
    }
    test_endpoint("POST", "/webhook/test/tgaraouy", data=test_webhook_data)
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")
    print("📊 Check the results above to see which endpoints are working")
    print("🌐 Visit http://localhost:8000/docs for interactive API documentation")

if __name__ == "__main__":
    main()
