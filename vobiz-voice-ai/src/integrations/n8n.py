"""
n8n Automation Integration
Triggers post-call workflows for CRM, SMS, Calendar, WhatsApp
"""

import httpx
from typing import Dict, Any, Optional
from datetime import datetime
import structlog
from ..config import settings

logger = structlog.get_logger()


class N8NClient:
    """
    Client for n8n webhook automation
    Triggers workflows for post-call processing
    """
    
    def __init__(self):
        self.webhook_url = settings.N8N_WEBHOOK_URL
        self.auth_header = settings.N8N_AUTH_HEADER
        self.headers = {
            "Content-Type": "application/json"
        }
        if self.auth_header:
            self.headers["Authorization"] = self.auth_header
    
    async def trigger_post_call_workflow(
        self,
        call_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Trigger n8n workflow to process completed call
        
        Args:
            call_data: Complete call data including:
                - call_id
                - business_id
                - caller_phone
                - transcript
                - summary
                - booking_created
                - appointment_details (if any)
                - duration_seconds
                - intent_detected
                - escalated_to_human
                
        Returns:
            Workflow execution result
        """
        logger.info("Triggering n8n post-call workflow",
                   call_id=call_data.get("call_id"),
                   business_id=call_data.get("business_id"))
        
        payload = {
            "event": "call.completed",
            "timestamp": datetime.utcnow().isoformat(),
            "data": call_data
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.webhook_url,
                    json=payload,
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info("n8n workflow triggered successfully",
                               call_id=call_data.get("call_id"),
                               workflow_result=result)
                    return result
                else:
                    error_text = response.text
                    logger.error("Failed to trigger n8n workflow",
                                status=response.status_code,
                                error=error_text)
                    # Don't raise - this is non-critical
                    return {"status": "failed", "error": error_text}
                    
        except httpx.TimeoutException:
            logger.warning("n8n webhook timeout",
                          call_id=call_data.get("call_id"))
            return {"status": "timeout"}
        except Exception as e:
            logger.error("n8n webhook error",
                        call_id=call_data.get("call_id"),
                        error=str(e))
            return {"status": "error", "error": str(e)}
    
    async def trigger_appointment_reminder(
        self,
        appointment_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Trigger n8n workflow to send appointment reminder
        
        Args:
            appointment_data: Appointment details including:
                - appointment_id
                - patient_name
                - patient_phone
                - appointment_date
                - appointment_time
                - clinic_name
                - service_type
                
        Returns:
            Reminder execution result
        """
        logger.info("Triggering appointment reminder",
                   appointment_id=appointment_data.get("appointment_id"),
                   patient=appointment_data.get("patient_name"))
        
        payload = {
            "event": "appointment.reminder",
            "timestamp": datetime.utcnow().isoformat(),
            "data": appointment_data
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.webhook_url}/reminder",
                    json=payload,
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info("Appointment reminder sent",
                               appointment_id=appointment_data.get("appointment_id"))
                    return result
                else:
                    logger.error("Failed to send reminder",
                                status=response.status_code)
                    return {"status": "failed"}
                    
        except Exception as e:
            logger.error("Reminder error", error=str(e))
            return {"status": "error", "error": str(e)}
    
    async def trigger_missed_call_followup(
        self,
        missed_call_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Trigger n8n workflow to follow up on missed calls
        
        Args:
            missed_call_data: Missed call details including:
                - call_id
                - caller_phone
                - business_id
                - call_time
                - reason (optional)
                
        Returns:
            Follow-up execution result
        """
        logger.info("Triggering missed call follow-up",
                   call_id=missed_call_data.get("call_id"),
                   caller=missed_call_data.get("caller_phone"))
        
        payload = {
            "event": "call.missed",
            "timestamp": datetime.utcnow().isoformat(),
            "data": missed_call_data
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.webhook_url}/missed-call",
                    json=payload,
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info("Missed call follow-up initiated",
                               call_id=missed_call_data.get("call_id"))
                    return result
                else:
                    logger.error("Failed to follow up missed call",
                                status=response.status_code)
                    return {"status": "failed"}
                    
        except Exception as e:
            logger.error("Missed call follow-up error", error=str(e))
            return {"status": "error", "error": str(e)}
    
    async def trigger_crm_sync(
        self,
        contact_data: Dict[str, Any],
        interaction_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Trigger n8n workflow to sync contact/interaction to CRM
        
        Args:
            contact_data: Contact details (name, phone, email, etc.)
            interaction_data: Call interaction details
            
        Returns:
            CRM sync result
        """
        logger.info("Triggering CRM sync",
                   contact_phone=contact_data.get("phone"))
        
        payload = {
            "event": "crm.sync",
            "timestamp": datetime.utcnow().isoformat(),
            "contact": contact_data,
            "interaction": interaction_data
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.webhook_url}/crm-sync",
                    json=payload,
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    result = response.json()
                    logger.info("CRM sync completed",
                               contact_phone=contact_data.get("phone"))
                    return result
                else:
                    logger.error("CRM sync failed",
                                status=response.status_code)
                    return {"status": "failed"}
                    
        except Exception as e:
            logger.error("CRM sync error", error=str(e))
            return {"status": "error", "error": str(e)}


# Singleton instance
_n8n_client: Optional[N8NClient] = None


def get_n8n_client() -> N8NClient:
    """Get or create n8n client singleton"""
    global _n8n_client
    if _n8n_client is None:
        _n8n_client = N8NClient()
    return _n8n_client


# Example workflow payloads for documentation
WORKFLOW_EXAMPLES = {
    "post_call": {
        "event": "call.completed",
        "data": {
            "call_id": "call_123",
            "business_id": "biz_456",
            "caller_phone": "+919876543210",
            "transcript": "Patient wants to book cleaning...",
            "summary": "Appointment booked for cleaning on 2024-01-20 at 3 PM",
            "booking_created": True,
            "duration_seconds": 180,
            "intent_detected": "appointment_booking"
        }
    },
    "appointment_reminder": {
        "event": "appointment.reminder",
        "data": {
            "appointment_id": "apt_789",
            "patient_name": "Rajesh Kumar",
            "patient_phone": "+919876543210",
            "appointment_date": "2024-01-20",
            "appointment_time": "15:00",
            "clinic_name": "Smile Dental Clinic",
            "service_type": "Dental Cleaning"
        }
    },
    "missed_call": {
        "event": "call.missed",
        "data": {
            "call_id": "call_999",
            "caller_phone": "+919876543210",
            "business_id": "biz_456",
            "call_time": "2024-01-15T18:30:00Z",
            "reason": "after_hours"
        }
    }
}
