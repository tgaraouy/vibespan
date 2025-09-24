#!/usr/bin/env python3
"""
Webhook API Routes for Vibespan.ai
Handles incoming webhook data from various health platforms.
"""

from fastapi import APIRouter, Request, HTTPException, Header
from typing import Dict, Any, Optional
import json
import hmac
import hashlib
import logging

from ..data.realtime_ingestion import get_ingestion_handler
from ..auth.tenant_manager import tenant_manager

router = APIRouter()
logger = logging.getLogger(__name__)

def extract_tenant_from_webhook(request: Request) -> str:
    """Extract tenant ID from webhook URL or headers"""
    # Try to get from URL path
    path_parts = request.url.path.split("/")
    if len(path_parts) >= 3 and path_parts[1] == "webhook":
        tenant_id = path_parts[2]
        if tenant_manager.get_tenant(tenant_id):
            return tenant_id
    
    # Try to get from headers
    tenant_header = request.headers.get("X-Tenant-ID")
    if tenant_header and tenant_manager.get_tenant(tenant_header):
        return tenant_header
    
    raise HTTPException(status_code=400, detail="Unable to determine tenant from webhook")

@router.post("/webhook/whoop/{tenant_id}")
async def whoop_webhook(tenant_id: str, request: Request, 
                       x_whoop_signature: Optional[str] = Header(None)):
    """WHOOP v2 webhook endpoint"""
    try:
        # Verify tenant exists
        tenant_config = tenant_manager.get_tenant(tenant_id)
        if not tenant_config:
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        # Get webhook data
        webhook_data = await request.json()
        
        # Verify signature (in production, implement proper signature verification)
        if x_whoop_signature:
            # TODO: Implement WHOOP signature verification
            logger.info(f"WHOOP signature received: {x_whoop_signature}")
        
        # Get ingestion handler
        ingestion_handler = get_ingestion_handler(tenant_id)
        
        # Process the webhook data
        result = await ingestion_handler.ingest_webhook_data("whoop_v2", webhook_data)
        
        # Log webhook receipt
        tenant_manager.log_audit(tenant_id, "whoop_webhook_received", {
            "records_processed": result.get("records_processed", 0),
            "timestamp": result.get("timestamp")
        })
        
        return {
            "status": "success",
            "message": "WHOOP webhook processed successfully",
            "tenant_id": tenant_id,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"WHOOP webhook error for tenant {tenant_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook/apple-health/{tenant_id}")
async def apple_health_webhook(tenant_id: str, request: Request):
    """Apple Health webhook endpoint"""
    try:
        # Verify tenant exists
        tenant_config = tenant_manager.get_tenant(tenant_id)
        if not tenant_config:
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        # Get webhook data
        webhook_data = await request.json()
        
        # Get ingestion handler
        ingestion_handler = get_ingestion_handler(tenant_id)
        
        # Process the webhook data
        result = await ingestion_handler.ingest_webhook_data("apple_health", webhook_data)
        
        # Log webhook receipt
        tenant_manager.log_audit(tenant_id, "apple_health_webhook_received", {
            "records_processed": result.get("records_processed", 0),
            "timestamp": result.get("timestamp")
        })
        
        return {
            "status": "success",
            "message": "Apple Health webhook processed successfully",
            "tenant_id": tenant_id,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Apple Health webhook error for tenant {tenant_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook/generic/{tenant_id}")
async def generic_webhook(tenant_id: str, request: Request, 
                         source: str = "generic"):
    """Generic webhook endpoint for custom integrations"""
    try:
        # Verify tenant exists
        tenant_config = tenant_manager.get_tenant(tenant_id)
        if not tenant_config:
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        # Get webhook data
        webhook_data = await request.json()
        
        # Get ingestion handler
        ingestion_handler = get_ingestion_handler(tenant_id)
        
        # Process the webhook data
        result = await ingestion_handler.ingest_webhook_data(source, webhook_data)
        
        # Log webhook receipt
        tenant_manager.log_audit(tenant_id, "generic_webhook_received", {
            "source": source,
            "records_processed": result.get("records_processed", 0),
            "timestamp": result.get("timestamp")
        })
        
        return {
            "status": "success",
            "message": f"{source} webhook processed successfully",
            "tenant_id": tenant_id,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Generic webhook error for tenant {tenant_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/webhook/status/{tenant_id}")
async def webhook_status(tenant_id: str):
    """Get webhook ingestion status for a tenant"""
    try:
        # Verify tenant exists
        tenant_config = tenant_manager.get_tenant(tenant_id)
        if not tenant_config:
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        # Get ingestion handler
        ingestion_handler = get_ingestion_handler(tenant_id)
        
        # Get status
        status = await ingestion_handler.get_ingestion_status()
        
        return status
        
    except Exception as e:
        logger.error(f"Webhook status error for tenant {tenant_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook/test/{tenant_id}")
async def test_webhook(tenant_id: str, test_data: Dict[str, Any]):
    """Test webhook endpoint for development"""
    try:
        # Verify tenant exists
        tenant_config = tenant_manager.get_tenant(tenant_id)
        if not tenant_config:
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        # Get ingestion handler
        ingestion_handler = get_ingestion_handler(tenant_id)
        
        # Process test data
        result = await ingestion_handler.ingest_webhook_data("test", test_data)
        
        return {
            "status": "success",
            "message": "Test webhook processed successfully",
            "tenant_id": tenant_id,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Test webhook error for tenant {tenant_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
