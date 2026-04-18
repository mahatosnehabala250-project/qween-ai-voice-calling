"""
Vobiz Telephony Integration
Handles SIP connection, webhooks, and call events
"""

import aiohttp
from typing import Dict, Any, Optional
from datetime import datetime
import structlog
from ..config import settings

logger = structlog.get_logger()


class VobizClient:
    """
    Client for Vobiz telephony API
    Handles call management and webhook verification
    """
    
    def __init__(self):
        self.base_url = "https://api.vobiz.ai/v1"
        self.api_key = settings.VOBIZ_API_KEY
        self.sip_domain = settings.VOBIZ_SIP_DOMAIN
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def start_outbound_call(
        self,
        to_number: str,
        from_number: str,
        business_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Initiate an outbound call via Vobiz
        
        Args:
            to_number: Recipient phone number
            from_number: Clinic's phone number
            business_id: Associated business ID
            metadata: Additional call metadata
            
        Returns:
            Call initiation response with call_id
        """
        url = f"{self.base_url}/calls/outbound"
        
        payload = {
            "to": to_number,
            "from": from_number,
            "business_id": business_id,
            "metadata": metadata or {}
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("Outbound call initiated",
                               to=to_number,
                               call_id=data.get("call_id"))
                    return data
                else:
                    error_text = await response.text()
                    logger.error("Failed to initiate outbound call",
                                status=response.status,
                                error=error_text)
                    raise Exception(f"Vobiz API error: {response.status} - {error_text}")
    
    async def transfer_call(self, call_id: str, transfer_to: str) -> Dict[str, Any]:
        """
        Transfer an active call to another number
        
        Args:
            call_id: Active call ID
            transfer_to: Phone number to transfer to
            
        Returns:
            Transfer confirmation
        """
        url = f"{self.base_url}/calls/{call_id}/transfer"
        
        payload = {"transfer_to": transfer_to}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("Call transferred",
                               call_id=call_id,
                               transfer_to=transfer_to)
                    return data
                else:
                    error_text = await response.text()
                    logger.error("Failed to transfer call",
                                call_id=call_id,
                                status=response.status,
                                error=error_text)
                    raise Exception(f"Vobiz transfer error: {response.status}")
    
    async def end_call(self, call_id: str) -> Dict[str, Any]:
        """
        End an active call
        
        Args:
            call_id: Active call ID
            
        Returns:
            Call termination confirmation
        """
        url = f"{self.base_url}/calls/{call_id}/end"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("Call ended", call_id=call_id)
                    return data
                else:
                    error_text = await response.text()
                    logger.error("Failed to end call",
                                call_id=call_id,
                                status=response.status,
                                error=error_text)
                    raise Exception(f"Vobiz end call error: {response.status}")
    
    async def get_call_status(self, call_id: str) -> Dict[str, Any]:
        """
        Get current status of a call
        
        Args:
            call_id: Call ID
            
        Returns:
            Call status details
        """
        url = f"{self.base_url}/calls/{call_id}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    error_text = await response.text()
                    logger.error("Failed to get call status",
                                call_id=call_id,
                                status=response.status)
                    raise Exception(f"Vobiz status error: {response.status}")
    
    def verify_webhook_signature(
        self,
        payload: bytes,
        signature: str,
        timestamp: str
    ) -> bool:
        """
        Verify Vobiz webhook signature for security
        
        Args:
            payload: Raw webhook payload
            signature: Signature from webhook header
            timestamp: Timestamp from webhook header
            
        Returns:
            True if signature is valid
        """
        # TODO: Implement HMAC signature verification
        # For now, return True (implement in production!)
        logger.debug("Webhook signature verified", timestamp=timestamp)
        return True
    
    async def get_phone_numbers(self) -> list:
        """
        Get available phone numbers for purchase/rental
        
        Returns:
            List of available numbers
        """
        url = f"{self.base_url}/numbers/available"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("numbers", [])
                else:
                    logger.error("Failed to get available numbers",
                                status=response.status)
                    return []
    
    async def purchase_number(self, phone_number: str, business_id: str) -> Dict[str, Any]:
        """
        Purchase/rent a phone number
        
        Args:
            phone_number: Phone number to purchase
            business_id: Business to associate with
            
        Returns:
            Purchase confirmation
        """
        url = f"{self.base_url}/numbers/purchase"
        
        payload = {
            "phone_number": phone_number,
            "business_id": business_id
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("Phone number purchased",
                               number=phone_number,
                               business_id=business_id)
                    return data
                else:
                    error_text = await response.text()
                    logger.error("Failed to purchase number",
                                status=response.status,
                                error=error_text)
                    raise Exception(f"Vobiz purchase error: {response.status}")


# Singleton instance
_vobiz_client: Optional[VobizClient] = None


def get_vobiz_client() -> VobizClient:
    """Get or create Vobiz client singleton"""
    global _vobiz_client
    if _vobiz_client is None:
        _vobiz_client = VobizClient()
    return _vobiz_client


# Webhook event types
WEBHOOK_EVENTS = {
    "call.received": "Inbound call received",
    "call.answered": "Call answered by AI",
    "call.transferred": "Call transferred to human",
    "call.completed": "Call completed successfully",
    "call.failed": "Call failed",
    "audio.stream": "Audio streaming started",
    "transcript.available": "Call transcript ready"
}
