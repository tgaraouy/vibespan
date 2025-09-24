#!/usr/bin/env python3
"""
Real-time Data Ingestion for Vibespan.ai
Handles webhook data ingestion and real-time processing.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import asyncio

from ..auth.tenant_manager import tenant_manager
from ..agents.agent_orchestrator import get_orchestrator

logger = logging.getLogger(__name__)

class RealTimeIngestion:
    """Handles real-time data ingestion from various sources"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.logger = logging.getLogger(f"RealTimeIngestion_{tenant_id}")
        self.processing_queue = asyncio.Queue()
    
    async def ingest_webhook_data(self, source: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest data from webhook"""
        self.logger.info(f"Ingesting webhook data from {source}")
        
        # Validate tenant
        tenant_config = tenant_manager.get_tenant(self.tenant_id)
        if not tenant_config:
            raise ValueError(f"Tenant {self.tenant_id} not found")
        
        # Process the data
        processed_data = await self._process_webhook_data(source, data)
        
        # Store the data
        storage_result = await self._store_ingested_data(source, processed_data)
        
        # Trigger agent processing
        agent_result = await self._trigger_agent_processing(processed_data)
        
        return {
            "ingestion_status": "success",
            "source": source,
            "records_processed": len(processed_data.get("records", [])),
            "storage_result": storage_result,
            "agent_processing": agent_result,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def _process_webhook_data(self, source: str, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw webhook data into standardized format"""
        
        if source == "whoop_v2":
            return await self._process_whoop_data(raw_data)
        elif source == "apple_health":
            return await self._process_apple_health_data(raw_data)
        else:
            # Generic processing
            return {
                "source": source,
                "records": [{
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": raw_data,
                    "processed_at": datetime.utcnow().isoformat()
                }]
            }
    
    async def _process_whoop_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process WHOOP v2 webhook data"""
        records = []
        
        # Extract different data types from WHOOP
        if "recovery" in raw_data:
            records.append({
                "type": "recovery",
                "timestamp": raw_data["recovery"].get("timestamp"),
                "data": {
                    "recovery_score": raw_data["recovery"].get("score"),
                    "hrv": raw_data["recovery"].get("hrv"),
                    "resting_heart_rate": raw_data["recovery"].get("resting_heart_rate")
                }
            })
        
        if "sleep" in raw_data:
            records.append({
                "type": "sleep",
                "timestamp": raw_data["sleep"].get("timestamp"),
                "data": {
                    "duration": raw_data["sleep"].get("duration"),
                    "efficiency": raw_data["sleep"].get("efficiency"),
                    "stages": raw_data["sleep"].get("stages", {})
                }
            })
        
        if "workout" in raw_data:
            records.append({
                "type": "workout",
                "timestamp": raw_data["workout"].get("timestamp"),
                "data": {
                    "strain": raw_data["workout"].get("strain"),
                    "activity_type": raw_data["workout"].get("activity_type"),
                    "duration": raw_data["workout"].get("duration")
                }
            })
        
        return {
            "source": "whoop_v2",
            "records": records,
            "processed_at": datetime.utcnow().isoformat()
        }
    
    async def _process_apple_health_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process Apple Health webhook data"""
        records = []
        
        # Extract health metrics
        for metric_type, metric_data in raw_data.items():
            if isinstance(metric_data, list):
                for data_point in metric_data:
                    records.append({
                        "type": metric_type,
                        "timestamp": data_point.get("timestamp"),
                        "data": data_point
                    })
            else:
                records.append({
                    "type": metric_type,
                    "timestamp": metric_data.get("timestamp"),
                    "data": metric_data
                })
        
        return {
            "source": "apple_health",
            "records": records,
            "processed_at": datetime.utcnow().isoformat()
        }
    
    async def _store_ingested_data(self, source: str, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Store ingested data in tenant's data directory"""
        try:
            # Get tenant data directory
            data_dir = tenant_manager.get_tenant_data_path(self.tenant_id, "raw")
            
            # Create timestamped file
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"{source}_{timestamp}.json"
            file_path = data_dir / filename
            
            # Store the data
            with open(file_path, "w") as f:
                json.dump(processed_data, f, indent=2)
            
            # Log audit
            tenant_manager.log_audit(self.tenant_id, "data_ingested", {
                "source": source,
                "records": len(processed_data.get("records", [])),
                "file": filename
            })
            
            return {
                "status": "stored",
                "file": filename,
                "records": len(processed_data.get("records", []))
            }
            
        except Exception as e:
            self.logger.error(f"Failed to store data: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _trigger_agent_processing(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger agent processing of the ingested data"""
        try:
            # Get orchestrator
            orchestrator = get_orchestrator(self.tenant_id)
            
            # Prepare data for agents
            agent_data = {
                "source": processed_data.get("source"),
                "records": processed_data.get("records", []),
                "timestamp": processed_data.get("processed_at")
            }
            
            # Process through agents
            results = orchestrator.process_health_data(agent_data)
            
            return {
                "status": "processed",
                "agents_used": results.get("agents_processed", []),
                "insights_generated": len(results.get("insights", [])),
                "recommendations": len(results.get("recommendations", []))
            }
            
        except Exception as e:
            self.logger.error(f"Failed to process with agents: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def get_ingestion_status(self) -> Dict[str, Any]:
        """Get ingestion status for the tenant"""
        try:
            # Get recent ingestion files
            data_dir = tenant_manager.get_tenant_data_path(self.tenant_id, "raw")
            ingestion_files = list(data_dir.glob("*_*.json"))
            
            # Analyze recent activity
            recent_files = sorted(ingestion_files, key=lambda x: x.stat().st_mtime, reverse=True)[:10]
            
            sources = {}
            total_records = 0
            
            for file_path in recent_files:
                try:
                    with open(file_path, "r") as f:
                        data = json.load(f)
                    
                    if isinstance(data, list):
                        source = data[0].get("source", "unknown") if data else "unknown"
                        record_count = len(data)
                    else:
                        source = data.get("source", "unknown")
                        record_count = len(data.get("records", []))
                    
                    if source not in sources:
                        sources[source] = {"files": 0, "records": 0}
                    
                    sources[source]["files"] += 1
                    sources[source]["records"] += record_count
                    total_records += record_count
                    
                except Exception as e:
                    self.logger.error(f"Error reading file {file_path}: {str(e)}")
            
            return {
                "tenant_id": self.tenant_id,
                "total_files": len(ingestion_files),
                "recent_files": len(recent_files),
                "total_records": total_records,
                "sources": sources,
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get ingestion status: {str(e)}")
            return {"error": str(e)}

# Global ingestion instances
_ingestion_handlers: Dict[str, RealTimeIngestion] = {}

def get_ingestion_handler(tenant_id: str) -> RealTimeIngestion:
    """Get or create ingestion handler for tenant"""
    if tenant_id not in _ingestion_handlers:
        _ingestion_handlers[tenant_id] = RealTimeIngestion(tenant_id)
    
    return _ingestion_handlers[tenant_id]
