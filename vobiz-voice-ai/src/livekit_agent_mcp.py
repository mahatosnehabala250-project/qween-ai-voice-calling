"""
LiveKit Voice AI Agent for Indian Dental Clinics
Stack: LiveKit Agents + Gemini 2.5 Flash Live + MCP + Vobiz
Language: Hindi/English (Hinglish)
Persona: Dr. Priya (Dental Assistant)
"""

import asyncio
import os
from livekit import agents, rtc
from livekit.agents import JobContext, WorkerOptions, cli, llm
from livekit.plugins import deepgram, elevenlabs, silero
from google import genai
from google.genai import types
import json

# --- CONFIGURATION ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
VOBIZ_SIP_URI = os.getenv("VOBIZ_SIP_URI", "sip:vobiz-trunk") # Configured in LiveKit Dashboard
CLINIC_NAME = os.getenv("CLINIC_NAME", "Smile Care Dental Clinic")

# --- MCP TOOLS DEFINITION (Simulated for now, can connect to real MCP servers) ---
# In production, these would connect to an MCP server running n8n or local tools
TOOLS = [
    {
        "name": "check_appointment_availability",
        "description": "Check if a specific time slot is available for booking.",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                "time": {"type": "string", "description": "Time in HH:MM format"}
            },
            "required": ["date", "time"]
        }
    },
    {
        "name": "book_appointment",
        "description": "Book an appointment for a patient.",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_name": {"type": "string"},
                "phone": {"type": "string"},
                "date": {"type": "string"},
                "time": {"type": "string"},
                "reason": {"type": "string"}
            },
            "required": ["patient_name", "phone", "date", "time"]
        }
    },
    {
        "name": "transfer_to_human",
        "description": "Transfer the call to a human receptionist if the user is angry or request is complex.",
        "parameters": {
            "type": "object",
            "properties": {
                "reason": {"type": "string"}
            },
            "required": ["reason"]
        }
    }
]

# --- GEMINI 2.5 FLASH LIVE CONFIGURATION ---
# Note: LiveKit currently has native plugins for Deepgram/ElevenLabs. 
# For Gemini 2.5 Live (Multimodal), we use the raw Google GenAI SDK within a custom STT/LLM/TTS loop 
# OR use LiveKit's new 'google' plugin if available. 
# Since Gemini 2.5 Live is very new, we will implement a custom Agent logic that streams audio to Gemini.

class DentalAssistant(agents.Agent):
    def __init__(self):
        super().__init__(
            instructions=(
                "You are Dr. Priya, a warm and professional dental assistant for " + CLINIC_NAME + ".\n"
                "You speak fluent Hindi, English, and Hinglish (mix of both).\n"
                "Your goal is to book appointments, answer FAQs about dental services, and handle emergencies.\n"
                "Keep responses short (under 2 sentences) to minimize latency.\n"
                "If the user speaks Hindi, reply in Hindi. If English, reply in English.\n"
                "Always confirm details before booking.\n"
                "If the user is angry or asks for something you can't do, use the transfer_to_human tool."
            )
        )
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    async def entrypoint(self, job: JobContext):
        # Initial greeting
        await job.say("Namaste! Main Dr. Priya bol rahi hoon. Kaise madad kar sakti hoon aaj?")

        # Create a room for the call
        room = job.room
        
        # Subscribe to audio tracks
        @room.on("track_subscribed")
        def on_track_subscribed(track, publication, participant):
            if track.kind == rtc.TrackKind.KIND_AUDIO:
                asyncio.create_task(self.handle_audio_stream(track, participant))

    async def handle_audio_stream(self, track: rtc.RemoteAudioTrack, participant: rtc.RemoteParticipant):
        """
        Streams audio from LiveKit to Gemini 2.5 Live API and sends response back.
        This is the core 'Real-time' loop.
        """
        audio_stream = track.stream()
        
        # Initialize Gemini Real-time Session
        # Note: This requires the specific 'live' endpoint which handles bidirectional audio
        session = self.client.aio.live.connect(
            model="gemini-2.5-flash-preview-live", # Using the preview live model ID
            config=types.LiveConnectConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Puck" # Or a Hindi-optimized voice if available
                    ))
                ),
                tools=[types.Tool(function_declarations=TOOLS)]
            )
        )

        async with session:
            # Task 1: Send Audio to Gemini
            async def send_audio():
                async for frame in audio_stream:
                    # Convert LiveKit AudioFrame to bytes expected by Gemini
                    await session.send_input(audio=frame.data.tobytes())
            
            # Task 2: Receive Response from Gemini
            async def receive_response():
                async for response in session.receive():
                    if response.server_content and response.server_content.model_turn:
                        for part in response.server_content.model_turn.parts:
                            if part.text:
                                # If text only (rare in live mode but possible)
                                await self.say(part.text)
                            elif part.inline_data and part.inline_data.mime_type.startswith("audio"):
                                # Play audio directly
                                await self.play_audio(part.inline_data.data)
                    
                    # Handle Tool Calls
                    if response.tool_call:
                        for call in response.tool_call.function_calls:
                            result = await self.execute_tool(call.name, call.args)
                            await session.send_tool_response(call.id, result)

            await asyncio.gather(send_audio(), receive_response())

    async def execute_tool(self, name: str, args: dict):
        print(f"Executing tool: {name} with args: {args}")
        
        if name == "check_appointment_availability":
            # Mock logic - Connect to n8n/MCP here
            return json.dumps({"available": True, "slot": f"{args['date']} at {args['time']}"})
        
        elif name == "book_appointment":
            # Trigger n8n webhook
            # requests.post(os.getenv("N8N_WEBHOOK_URL"), json=args)
            return json.dumps({"success": True, "confirmation_id": "DK-12345"})
            
        elif name == "transfer_to_human":
            # Logic to transfer SIP call via LiveKit SIP API
            await self.transfer_call("+919876543210") # Receptionist number
            return json.dumps({"status": "transferring"})
            
        return json.dumps({"error": "Tool not found"})

    async def play_audio(self, audio_data: bytes):
        """Send audio bytes back to the LiveKit room"""
        source = rtc.AudioSource(24000, 1)
        track = rtc.LocalAudioTrack.create_audio_track("agent-mic", source)
        options = rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_MICROPHONE)
        await self.job.room.local_participant.publish_track(track, options)
        
        # Push frames to source (simplified for brevity)
        # In production, chunk audio_data into 10ms frames
        frame = rtc.AudioFrame(data=audio_data, sample_rate=24000, num_channels=1, samples_per_channel=len(audio_data)//2)
        await source.capture_frame(frame)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=DentalAssistant))
