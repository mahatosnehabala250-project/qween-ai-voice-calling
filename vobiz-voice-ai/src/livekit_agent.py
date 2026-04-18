"""
LiveKit Agent with MCP Integration for Vobiz Voice AI Platform
Connects Vobiz SIP → LiveKit → Gemini 2.5 Flash Live → n8n Automation
Optimized for Indian Dental Clinics (Hindi/English)
"""

import asyncio
import os
import logging
from typing import Optional
from datetime import datetime

# LiveKit imports
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import google, silero, deepgram
from livekit.plugins.google.models import _models

# MCP (Model Context Protocol) imports
try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("MCP not installed, running without tool integration")

# Custom integrations
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.integrations.gemini_live import GeminiLiveClient
from src.integrations.n8n import N8NClient
from src.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DentalClinicAgent:
    """
    Voice AI Agent for Dental Clinics
    - Handles appointment booking
    - Answers FAQs
    - Manages missed calls
    - Supports Hindi & English
    """
    
    def __init__(self, ctx: JobContext):
        self.ctx = ctx
        self.clinic_id = ctx.job.id  # Will be overridden by metadata
        self.mcp_session: Optional[ClientSession] = None
        self.n8n_client = N8NClient()
        
        # Initialize Gemini 2.5 Flash Live
        # Using Google's native plugin for LiveKit
        self.llm = google.LLM(model="gemini-2.5-flash-preview-native-audio-dialog")
        
        # STT is handled by Gemini Live (native audio)
        # But we add Deepgram as fallback if needed
        self.stt = deepgram.STT(model="nova-2", language="hi")
        
        # TTS is handled by Gemini Live (native audio)
        # But we add Silero as fallback
        self.tts = silero.TTS(language="hi")
        
        # Voice Assistant configuration
        self.assistant = VoiceAssistant(
            chat_ctx=self._create_initial_chat_context(),
            fnc_ctx=self._create_function_context(),
            llm=self.llm,
            tts=self.tts,  # Will be overridden by Gemini Live audio
            min_endpointing_delay=0.5,
        )
        
    def _create_initial_chat_context(self) -> llm.ChatContext:
        """Create persona for dental clinic assistant"""
        return llm.ChatContext().append(
            role="system",
            text=(
                "You are Dr. Priya, a friendly and professional dental clinic assistant in India. "
                "You speak fluent Hindi and English (Hinglish). "
                "Your goal is to help patients book appointments, answer questions about services, "
                "and handle emergency situations appropriately.\n\n"
                "Services offered:\n"
                "- General Checkup (₹500)\n"
                "- Teeth Cleaning (₹1,200)\n"
                "- Root Canal (₹3,500)\n"
                "- Teeth Whitening (₹5,000)\n"
                "- Emergency Dental Care (₹2,000)\n\n"
                "Clinic Hours: Mon-Sat 9 AM - 8 PM, Sun 10 AM - 2 PM\n"
                "Location: Mumbai, India\n\n"
                "Rules:\n"
                "1. Always confirm patient name and phone number before booking\n"
                "2. Never promise specific treatment without doctor consultation\n"
                "3. For emergencies (severe pain, bleeding), prioritize immediate appointment\n"
                "4. If unsure, offer to transfer to human receptionist\n"
                "5. Keep responses concise (under 30 seconds)\n"
                "6. Use warm, empathetic tone\n"
                "7. End calls with 'Thank you for calling! Have a great day!'"
            ),
        )
    
    def _create_function_context(self):
        """Define tools/functions the agent can call"""
        class FunctionContext:
            
            @llm.ai_callable(description="Book a dental appointment")
            async def book_appointment(
                self,
                patient_name: str,
                phone_number: str,
                preferred_date: str,
                preferred_time: str,
                service_type: str = "General Checkup",
            ):
                """Book appointment and trigger n8n workflow"""
                logger.info(f"Booking appointment: {patient_name}, {phone_number}, {preferred_date} {preferred_time}")
                
                # Trigger n8n webhook
                await self.n8n_client.trigger_workflow(
                    workflow_name="appointment-booking",
                    data={
                        "clinic_id": self.clinic_id,
                        "patient_name": patient_name,
                        "phone_number": phone_number,
                        "preferred_date": preferred_date,
                        "preferred_time": preferred_time,
                        "service_type": service_type,
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )
                
                return f"Appointment booked for {patient_name} on {preferred_date} at {preferred_time}. You'll receive a WhatsApp confirmation shortly!"
            
            @llm.ai_callable(description="Check available appointment slots")
            async def check_availability(
                self,
                date: str,
                service_type: str = "General Checkup",
            ):
                """Check calendar availability via MCP or n8n"""
                # For now, return mock availability
                # In production, integrate with Google Calendar via MCP
                available_slots = ["10:00 AM", "11:30 AM", "3:00 PM", "5:30 PM"]
                return f"Available slots on {date}: {', '.join(available_slots)}. Which time works for you?"
            
            @llm.ai_callable(description="Transfer call to human receptionist")
            async def transfer_to_human(
                self,
                reason: str,
            ):
                """Transfer call to human staff"""
                logger.info(f"Transferring call: {reason}")
                
                # Trigger n8n escalation workflow
                await self.n8n_client.trigger_workflow(
                    workflow_name="call-escalation",
                    data={
                        "clinic_id": self.clinic_id,
                        "reason": reason,
                        "timestamp": datetime.utcnow().isoformat(),
                    }
                )
                
                # Note: Actual SIP transfer handled by LiveKit/Vobiz
                return "Let me transfer you to our receptionist. Please hold..."
            
            @llm.ai_callable(description="Get clinic information (hours, location, services)")
            async def get_clinic_info(self, info_type: str):
                """Provide clinic information"""
                if info_type == "hours":
                    return "We're open Monday to Saturday 9 AM to 8 PM, and Sunday 10 AM to 2 PM."
                elif info_type == "location":
                    return "We're located in Bandra West, Mumbai, near the railway station."
                elif info_type == "services":
                    return "We offer general checkups, cleaning, root canals, whitening, and emergency care."
                else:
                    return "We provide comprehensive dental care. What specific service are you interested in?"
        
        return FunctionContext()
    
    async def initialize_mcp(self):
        """Initialize MCP session for advanced tool integration"""
        if not MCP_AVAILABLE:
            logger.warning("MCP not available, skipping initialization")
            return
        
        try:
            server_params = StdioServerParameters(
                command="python",
                args=["-m", "mcp_server_calendar"],  # Example: Google Calendar MCP server
                env={"GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY")},
            )
            
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    self.mcp_session = session
                    logger.info("MCP session initialized successfully")
        except Exception as e:
            logger.error(f"MCP initialization failed: {e}")
            self.mcp_session = None
    
    async def run(self):
        """Run the voice assistant"""
        # Connect to room
        await self.ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
        
        # Wait for participant
        logger.info("Waiting for participant...")
        
        # Start assistant
        await self.assistant.start(self.ctx.room)
        
        # Initial greeting
        await self.assistant.say("Namaste! Main Dr. Priya bol rahi hoon. Kaise madad kar sakti hoon aapki?")


async def entrypoint(ctx: JobContext):
    """LiveKit job entrypoint"""
    logger.info(f"Starting job: {ctx.job.id}")
    
    # Extract clinic ID from metadata
    clinic_id = ctx.job.metadata.get("clinic_id", "default")
    logger.info(f"Clinic ID: {clinic_id}")
    
    # Create and run agent
    agent = DentalClinicAgent(ctx)
    agent.clinic_id = clinic_id
    
    # Initialize MCP (optional)
    await agent.initialize_mcp()
    
    # Run the agent
    await agent.run()


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            worker_type="voice-assistant",
        )
    )
