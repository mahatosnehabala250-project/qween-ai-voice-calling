"""
Webhook Routes for Vobiz and n8n Integration
"""

from fastapi import APIRouter, HTTPException, Request, Header
from pydantic import BaseModel
from typing import Dict, Any, Optional
import structlog
import httpx
from ..config import settings

logger = structlog.get_logger()
router = APIRouter()

class VobizWebhookPayload(BaseModel):
    call_id: str
    business_id: str
    caller_phone: str
    event_type: str
    recording_url: Optional[str] = None
    transcript: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@router.post("/vobiz")
async def handle_vobiz_webhook(
    request: Request,
    payload: VobizWebhookPayload,
    x_vobiz_signature: Optional[str] = Header(None)
):
    """
    Receive webhook events from Vobiz (call completed, recording ready, etc.)
    """
    logger.info("Received Vobiz webhook",
                call_id=payload.call_id,
                event_type=payload.event_type)
    
    # Verify webhook signature (implement security check)
    # if not verify_vobiz_signature(x_vobiz_signature, payload):
    #     raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Process based on event type
    if payload.event_type == "call_completed":
        # Trigger n8n workflow for post-call processing
        await trigger_n8n_workflow(payload.dict())
    
    return {"status": "received", "call_id": payload.call_id}

async def trigger_n8n_workflow(call_data: Dict[str, Any]):
    """
    Send call data to n8n for post-call automation
    """
    try:
        async with httpx.AsyncClient() as client:
            headers = {}
            if settings.N8N_AUTH_HEADER:
                headers["Authorization"] = settings.N8N_AUTH_HEADER
            
            response = await client.post(
                settings.N8N_WEBHOOK_URL,
                json=call_data,
                headers=headers,
                timeout=10.0
            )
            
            logger.info("Triggered n8n workflow",
                       status_code=response.status_code)
    except Exception as e:
        logger.error("Failed to trigger n8n workflow", error=str(e))
        # Don't fail the request, just log the error
