"""
Gemini 2.5 Flash Live Integration
Handles real-time voice streaming with STT + LLM + TTS in one API
Optimized for Indian English + Hindi
"""

import asyncio
import base64
import json
import websockets
from typing import AsyncGenerator, Optional, Callable
from datetime import datetime
import structlog
from ..config import settings

logger = structlog.get_logger()

class GeminiLiveSession:
    """
    Manages a live session with Gemini 2.5 Flash
    Handles bidirectional audio streaming and response generation
    """
    
    def __init__(
        self,
        session_id: str,
        business_id: str,
        system_prompt: str,
        language_code: str = "en-IN",
        voice_id: str = "en-US-Standard-A"
    ):
        self.session_id = session_id
        self.business_id = business_id
        self.system_prompt = system_prompt
        self.language_code = language_code
        self.voice_id = voice_id
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.is_connected = False
        self.audio_queue = asyncio.Queue()
        self.response_callback: Optional[Callable] = None
        
    async def connect(self):
        """Establish connection to Gemini 2.5 Live API"""
        try:
            ws_url = f"wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key={settings.GOOGLE_API_KEY}"
            
            self.ws = await websockets.connect(ws_url)
            self.is_connected = True
            
            # Send initial configuration
            setup_message = {
                "setup": {
                    "model": settings.GEMINI_MODEL,
                    "system_instruction": {
                        "parts": [{
                            "text": self.system_prompt
                        }]
                    },
                    "generation_config": {
                        "response_modalities": ["AUDIO"],
                        "speech_config": {
                            "voice_config": {
                                "prebuilt_voice_config": {
                                    "voice_name": self.voice_id
                                }
                            }
                        }
                    },
                    "tools": [{
                        "google_search_retrieval": {}
                    }]
                }
            }
            
            await self.ws.send(json.dumps(setup_message))
            logger.info("Gemini Live session connected", 
                       session_id=self.session_id,
                       model=settings.GEMINI_MODEL)
            
        except Exception as e:
            logger.error("Failed to connect to Gemini Live", error=str(e))
            raise
    
    async def send_audio(self, audio_data: bytes):
        """Send audio chunk to Gemini for processing"""
        if not self.is_connected or not self.ws:
            raise RuntimeError("Session not connected")
        
        # Encode audio as base64
        audio_b64 = base64.b64encode(audio_data).decode('utf-8')
        
        message = {
            "realtime_input": {
                "media_chunks": [{
                    "data": audio_b64,
                    "mime_type": "audio/pcm"
                }]
            }
        }
        
        await self.ws.send(json.dumps(message))
    
    async def receive_responses(self) -> AsyncGenerator[dict, None]:
        """Listen for AI responses (transcripts + audio)"""
        if not self.ws:
            raise RuntimeError("Session not connected")
        
        async for message in self.ws:
            try:
                data = json.loads(message)
                
                # Handle server content (AI response)
                if "serverContent" in data:
                    content = data["serverContent"]
                    
                    # Extract transcript
                    transcript = ""
                    if "modelTurn" in content:
                        parts = content["modelTurn"].get("parts", [])
                        for part in parts:
                            if "text" in part:
                                transcript += part["text"]
                            elif "inlineData" in part:
                                # Audio data
                                audio_data = base64.b64decode(part["inlineData"]["data"])
                                yield {
                                    "type": "audio",
                                    "data": audio_data,
                                    "transcript": transcript
                                }
                    
                    if transcript:
                        yield {
                            "type": "transcript",
                            "text": transcript
                        }
                
                # Handle turn complete
                if "turnComplete" in data and data["turnComplete"]:
                    yield {"type": "turn_complete"}
                    
            except json.JSONDecodeError as e:
                logger.error("Failed to parse Gemini response", error=str(e))
                continue
    
    async def send_text(self, text: str):
        """Send text input (for testing or fallback)"""
        if not self.ws:
            raise RuntimeError("Session not connected")
        
        message = {
            "clientContent": {
                "turns": [{
                    "role": "user",
                    "parts": [{"text": text}]
                }],
                "turnComplete": True
            }
        }
        
        await self.ws.send(json.dumps(message))
    
    async def close(self):
        """Close the session gracefully"""
        if self.ws:
            await self.ws.close()
            self.is_connected = False
            logger.info("Gemini Live session closed", session_id=self.session_id)


class DentalClinicAgent:
    """
    Specialized agent for dental clinics
    Handles appointments, FAQs, emergencies in English + Hindi
    """
    
    SYSTEM_PROMPT = """
You are Dr. Priya, a friendly and professional dental assistant for an Indian dental clinic.
You speak fluent English and Hindi (Hinglish).

YOUR ROLE:
- Answer patient calls warmly and professionally
- Book, reschedule, or cancel appointments
- Answer common dental questions (pain, treatments, costs, timings)
- Handle emergencies appropriately
- Escalate complex cases to human staff

LANGUAGE:
- Default to English, but switch to Hindi if the caller prefers
- You can use Hinglish (mix of Hindi and English) naturally
- Example: "Hello! Main Dr. Priya bol rahi hoon. How can I help you today?"

APPOINTMENT BOOKING:
- Ask for: patient name, phone number, preferred date/time, service type
- Confirm all details before finalizing
- Use 12-hour format (e.g., "3:00 PM")
- Clinic hours: Mon-Sat, 9 AM - 8 PM

EMERGENCIES:
- Severe pain, bleeding, trauma → Transfer to emergency line immediately
- Reassure the patient first: "Don't worry, we'll help you right away"

TONE:
- Warm, empathetic, professional
- Use polite Hindi honorifics (aap, ji) when speaking Hindi
- Be patient with elderly callers

ESCALATION:
- If caller is angry/frustrated → Transfer to human
- If question is beyond your knowledge → Transfer to doctor
- If technical issue → Apologize and transfer

NEVER:
- Make up appointment times that don't exist
- Give medical advice beyond general information
- Promise specific treatment outcomes
- Discuss exact prices without consultation

START EVERY CALL:
"Hello! Thank you for calling [Clinic Name]. Main Dr. Priya bol rahi hoon. How can I help you today?"
"""
    
    def __init__(self, business_id: str, clinic_name: str = "Smile Dental Clinic"):
        self.business_id = business_id
        self.clinic_name = clinic_name
        self.session: Optional[GeminiLiveSession] = None
        self.call_metadata = {}
        
    async def start_call(self, call_id: str, caller_phone: str):
        """Initialize a new call session"""
        self.call_metadata = {
            "call_id": call_id,
            "caller_phone": caller_phone,
            "start_time": datetime.utcnow()
        }
        
        # Create Gemini session with customized prompt
        personalized_prompt = self.SYSTEM_PROMPT.replace("[Clinic Name]", self.clinic_name)
        
        self.session = GeminiLiveSession(
            session_id=call_id,
            business_id=self.business_id,
            system_prompt=personalized_prompt,
            language_code="en-IN",
            voice_id="en-IN-Standard-A"  # Indian English voice
        )
        
        await self.session.connect()
        logger.info("Dental clinic agent started", 
                   call_id=call_id,
                   clinic=self.clinic_name)
    
    async def process_audio(self, audio_chunk: bytes) -> AsyncGenerator[dict, None]:
        """Process incoming audio and yield AI responses"""
        if not self.session:
            raise RuntimeError("Agent not initialized")
        
        # Send audio to Gemini
        await self.session.send_audio(audio_chunk)
        
        # Receive and yield responses
        async for response in self.session.receive_responses():
            yield response
    
    async def handle_booking_request(self, booking_details: dict) -> dict:
        """
        Process appointment booking request
        Returns confirmation or error
        """
        # TODO: Integrate with calendar/CRM via n8n
        # For now, return mock confirmation
        
        return {
            "success": True,
            "appointment_id": "apt_123456",
            "message": f"Appointment booked for {booking_details.get('patient_name')} on {booking_details.get('date')} at {booking_details.get('time')}",
            "details": booking_details
        }
    
    async def end_call(self):
        """End the call and cleanup"""
        if self.session:
            await self.session.close()
        
        # Calculate call duration
        end_time = datetime.utcnow()
        duration = (end_time - self.call_metadata["start_time"]).total_seconds()
        
        logger.info("Call ended",
                   call_id=self.call_metadata["call_id"],
                   duration_seconds=duration)
        
        return {
            "call_id": self.call_metadata["call_id"],
            "duration_seconds": int(duration),
            "end_time": end_time.isoformat()
        }


# Helper function to create agent instance
def create_dental_agent(business_id: str, clinic_name: str = "Smile Dental Clinic") -> DentalClinicAgent:
    """Factory function to create a dental clinic agent"""
    return DentalClinicAgent(business_id, clinic_name)
