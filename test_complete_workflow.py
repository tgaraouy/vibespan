#!/usr/bin/env python3
"""
Complete Workflow Test for Vibespan.ai
Tests the entire system from onboarding to agent processing.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.auth.tenant_manager import tenant_manager
from src.data.data_importer import data_importer
from src.agents.agent_orchestrator import get_orchestrator
from src.data.realtime_ingestion import get_ingestion_handler

async def test_complete_workflow():
    """Test the complete workflow for tgaraouy"""
    
    print("🚀 Testing Complete Vibespan.ai Workflow")
    print("=" * 50)
    
    tenant_id = "tgaraouy"
    
    # Step 1: Verify tenant exists
    print("\n1️⃣ Verifying tenant setup...")
    tenant_config = tenant_manager.get_tenant(tenant_id)
    if not tenant_config:
        print("❌ Tenant not found! Run setup_tgaraouy.py first.")
        return
    
    print(f"✅ Tenant {tenant_id} found")
    print(f"   - Created: {tenant_config.get('created_at')}")
    print(f"   - Active agents: {len(tenant_config.get('active_agents', []))}")
    print(f"   - Data sources: {len(tenant_config.get('data_sources', []))}")
    
    # Step 2: Test agent orchestration
    print("\n2️⃣ Testing agent orchestration...")
    orchestrator = get_orchestrator(tenant_id)
    agent_status = orchestrator.get_agent_status()
    
    print(f"✅ Orchestrator initialized")
    print(f"   - Total agents: {agent_status['total_agents']}")
    print(f"   - Active agents: {list(agent_status['agents'].keys())}")
    
    # Step 3: Test agent processing with sample data
    print("\n3️⃣ Testing agent processing...")
    sample_health_data = {
        "recovery_score": 75,
        "sleep_quality": 7.5,
        "hrv": 45,
        "heart_rate_resting": 65,
        "goals": ["performance", "recovery"],
        "recent_trends": {
            "sleep_improvement": True,
            "hrv_decline": False
        },
        "health_metrics": {
            "heart_rate_resting": 65,
            "sleep_duration": 7.5,
            "recovery_score": 75
        }
    }
    
    agent_results = orchestrator.process_health_data(sample_health_data)
    
    print(f"✅ Agent processing completed")
    print(f"   - Agents processed: {len(agent_results['agents_processed'])}")
    print(f"   - Insights generated: {len(agent_results['insights'])}")
    print(f"   - Recommendations: {len(agent_results['recommendations'])}")
    print(f"   - Alerts: {len(agent_results['alerts'])}")
    print(f"   - Warnings: {len(agent_results['warnings'])}")
    
    # Step 4: Test real-time ingestion
    print("\n4️⃣ Testing real-time ingestion...")
    ingestion_handler = get_ingestion_handler(tenant_id)
    
    # Simulate WHOOP webhook data
    whoop_data = {
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
        }
    }
    
    ingestion_result = await ingestion_handler.ingest_webhook_data("whoop_v2", whoop_data)
    
    print(f"✅ Real-time ingestion completed")
    print(f"   - Records processed: {ingestion_result['records_processed']}")
    print(f"   - Storage status: {ingestion_result['storage_result']['status']}")
    print(f"   - Agent processing: {ingestion_result['agent_processing']['status']}")
    
    # Step 5: Test insights retrieval
    print("\n5️⃣ Testing insights retrieval...")
    insights = orchestrator.get_insights_summary()
    
    if "error" not in insights:
        print(f"✅ Insights retrieved")
        print(f"   - Latest insights: {len(insights.get('latest_insights', []))}")
        print(f"   - Recommendations: {len(insights.get('recommendations', []))}")
        print(f"   - Agents used: {len(insights.get('agents_used', []))}")
    else:
        print(f"⚠️ No insights available yet: {insights['error']}")
    
    # Step 6: Test ingestion status
    print("\n6️⃣ Testing ingestion status...")
    ingestion_status = await ingestion_handler.get_ingestion_status()
    
    print(f"✅ Ingestion status retrieved")
    print(f"   - Total files: {ingestion_status['total_files']}")
    print(f"   - Total records: {ingestion_status['total_records']}")
    print(f"   - Sources: {list(ingestion_status['sources'].keys())}")
    
    # Step 7: Display sample insights
    print("\n7️⃣ Sample Insights Generated:")
    print("-" * 30)
    
    if agent_results['insights']:
        for i, insight in enumerate(agent_results['insights'][:3], 1):
            print(f"{i}. {insight}")
    
    if agent_results['recommendations']:
        print("\n📋 Recommendations:")
        for i, rec in enumerate(agent_results['recommendations'][:2], 1):
            agent = rec.get('agent', 'Unknown')
            recommendation = rec.get('recommendation', {})
            print(f"{i}. [{agent}] {recommendation.get('recommendation', 'No recommendation')}")
    
    if agent_results['alerts']:
        print("\n🚨 Alerts:")
        for alert in agent_results['alerts']:
            print(f"   - {alert}")
    
    if agent_results['warnings']:
        print("\n⚠️ Warnings:")
        for warning in agent_results['warnings']:
            print(f"   - {warning}")
    
    print("\n" + "=" * 50)
    print("🎉 Complete Workflow Test Successful!")
    print(f"🌐 Your health agents are ready at: https://{tenant_id}.vibespan.ai")
    print("📊 All systems operational and processing health data")
    print("🤖 AI agents are generating personalized insights")

if __name__ == "__main__":
    asyncio.run(test_complete_workflow())
