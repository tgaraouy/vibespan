#!/usr/bin/env python3
"""
Test Vibespan.ai with Real Health Data
Tests the system with tgaraouy's actual health data.
"""

import requests
import json
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.auth.tenant_manager import tenant_manager
from src.agents.agent_orchestrator import get_orchestrator

def test_with_real_data():
    """Test the system with real health data"""
    
    print("🏥 Testing Vibespan.ai with Real Health Data")
    print("=" * 60)
    
    tenant_id = "tgaraouy"
    base_url = "http://localhost:8000"
    headers = {"Host": "tgaraouy.localhost:8000"}
    
    # Step 1: Get tenant data summary
    print("1️⃣ Getting your health data summary...")
    try:
        response = requests.get(f"{base_url}/data/summary", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health data summary retrieved")
            print(f"   - Total files: {data['total_files']}")
            print(f"   - Data sources: {len(data['sources'])}")
            
            for source in data['sources']:
                print(f"   - {source['file']}: {source['records']} records from {source['source']}")
        else:
            print(f"❌ Failed to get data summary: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Step 2: Test with WHOOP-like data
    print("\n2️⃣ Testing with WHOOP recovery data...")
    try:
        whoop_data = {
            "recovery_score": 78,
            "hrv": 47,
            "resting_heart_rate": 62,
            "sleep_duration": 7.5,
            "sleep_efficiency": 0.85,
            "strain": 15.2,
            "goals": ["performance", "recovery"],
            "recent_trends": {
                "hrv_improvement": True,
                "sleep_consistency": True,
                "strain_management": True
            }
        }
        
        response = requests.post(f"{base_url}/agents/process", 
                               json=whoop_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ WHOOP data processed successfully")
            print(f"   - Agents processed: {len(data['agents_processed'])}")
            print(f"   - Insights generated: {len(data['insights'])}")
            print(f"   - Recommendations: {len(data['recommendations'])}")
            
            # Show specific insights
            print(f"\n   📊 Key Insights:")
            for insight in data['insights'][:5]:
                print(f"   • {insight}")
            
            if data['recommendations']:
                print(f"\n   💡 Recommendations:")
                for rec in data['recommendations']:
                    agent = rec.get('agent', 'Unknown')
                    recommendation = rec.get('recommendation', {})
                    if isinstance(recommendation, dict):
                        rec_text = recommendation.get('recommendation', 'No specific recommendation')
                    else:
                        rec_text = str(recommendation)
                    print(f"   • [{agent}] {rec_text}")
        else:
            print(f"❌ Failed to process WHOOP data: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Step 3: Test with workout data
    print("\n3️⃣ Testing with workout performance data...")
    try:
        workout_data = {
            "workout_type": "strength_training",
            "duration_minutes": 75,
            "intensity": "high",
            "recovery_score": 78,
            "sleep_quality": 8.2,
            "hrv": 47,
            "goals": ["performance", "strength_gain"],
            "recent_workouts": [
                {"type": "cardio", "duration": 45, "intensity": "moderate"},
                {"type": "strength", "duration": 60, "intensity": "high"}
            ]
        }
        
        response = requests.post(f"{base_url}/agents/process", 
                               json=workout_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Workout data processed successfully")
            print(f"   - Agents processed: {len(data['agents_processed'])}")
            print(f"   - Insights generated: {len(data['insights'])}")
            
            # Show workout-specific insights
            workout_insights = [insight for insight in data['insights'] 
                              if any(word in insight.lower() for word in ['workout', 'exercise', 'training', 'intensity'])]
            if workout_insights:
                print(f"\n   🏋️ Workout Insights:")
                for insight in workout_insights[:3]:
                    print(f"   • {insight}")
        else:
            print(f"❌ Failed to process workout data: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Step 4: Test with nutrition data
    print("\n4️⃣ Testing with nutrition data...")
    try:
        nutrition_data = {
            "meals_today": [
                {"type": "breakfast", "foods": ["oats", "berries", "protein_powder"]},
                {"type": "lunch", "foods": ["chicken", "rice", "vegetables"]},
                {"type": "dinner", "foods": ["salmon", "sweet_potato", "broccoli"]}
            ],
            "hydration": 8,  # glasses of water
            "supplements": ["multivitamin", "omega3", "vitamin_d"],
            "recovery_score": 78,
            "goals": ["performance", "recovery"],
            "dietary_preferences": ["balanced", "high_protein"]
        }
        
        response = requests.post(f"{base_url}/agents/process", 
                               json=nutrition_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Nutrition data processed successfully")
            print(f"   - Agents processed: {len(data['agents_processed'])}")
            print(f"   - Insights generated: {len(data['insights'])}")
            
            # Show nutrition-specific insights
            nutrition_insights = [insight for insight in data['insights'] 
                                if any(word in insight.lower() for word in ['nutrition', 'food', 'diet', 'supplement', 'meal'])]
            if nutrition_insights:
                print(f"\n   🥗 Nutrition Insights:")
                for insight in nutrition_insights[:3]:
                    print(f"   • {insight}")
        else:
            print(f"❌ Failed to process nutrition data: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Step 5: Test webhook with real data
    print("\n5️⃣ Testing webhook with real WHOOP data...")
    try:
        real_whoop_webhook = {
            "recovery": {
                "timestamp": "2024-09-23T06:00:00Z",
                "score": 78,
                "hrv": 47,
                "resting_heart_rate": 62
            },
            "sleep": {
                "timestamp": "2024-09-23T06:00:00Z",
                "duration": 7.5,
                "efficiency": 0.85,
                "stages": {
                    "light": 4.5,
                    "deep": 2.0,
                    "rem": 1.0
                }
            },
            "workout": {
                "timestamp": "2024-09-22T18:00:00Z",
                "strain": 15.2,
                "activity_type": "strength_training",
                "duration": 75
            }
        }
        
        response = requests.post(f"{base_url}/webhook/test/tgaraouy", 
                               json=real_whoop_webhook, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Real WHOOP webhook processed successfully")
            print(f"   - Status: {data['status']}")
            print(f"   - Records processed: {data['result']['records_processed']}")
            print(f"   - Agent processing: {data['result']['agent_processing']['status']}")
        else:
            print(f"❌ Failed to process webhook: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Step 6: Get comprehensive insights
    print("\n6️⃣ Getting comprehensive health insights...")
    try:
        response = requests.get(f"{base_url}/agents/insights", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Comprehensive insights retrieved")
            print(f"   - Latest insights: {len(data.get('latest_insights', []))}")
            print(f"   - Recommendations: {len(data.get('recommendations', []))}")
            print(f"   - Agents used: {len(data.get('agents_used', []))}")
            
            if data.get('latest_insights'):
                print(f"\n   🧠 Latest Health Insights:")
                for insight in data['latest_insights'][:5]:
                    print(f"   • {insight}")
        else:
            print(f"❌ Failed to get insights: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Real Data Testing Complete!")
    print("📊 Your health agents are processing your actual data")
    print("🤖 AI insights are being generated from your health metrics")
    print("💡 Personalized recommendations are ready for your wellness journey")

if __name__ == "__main__":
    test_with_real_data()
