# Vobiz Integration Guide 📞

## Step 1: Sign Up for Vobiz
1. Visit https://vobiz.ai/
2. Create your account
3. Complete KYC verification (required for telephony)
4. Add payment method

## Step 2: Get Your Credentials
After signup, you'll need:
- **API Key**: For authentication
- **SIP Credentials**: Username, password, server URL
- **Webhook URL**: Where Vobiz will send call events

## Step 3: Set Up Your First Phone Number (DID)
```bash
# Example API call to get available numbers
curl -X GET "https://api.vobiz.ai/v1/numbers/available" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

## Step 4: Configure Webhook for Incoming Calls
Vobiz will send POST requests to your webhook when:
- Call comes in
- Call status changes
- Call ends

Your webhook endpoint should:
1. Receive the call event
2. Initiate STT (Speech-to-Text)
3. Send to LLM for response
4. Convert to speech (TTS)
5. Stream back to caller via Vobiz

## Step 5: Basic Architecture Flow
```
Caller → Vobiz (SIP) → Your Server → STT → LLM → TTS → Vobiz → Caller
                              ↓
                         PostgreSQL (log calls)
```

## Step 6: Test Your Setup
1. Buy a test number from Vobiz
2. Point webhook to your development server (use ngrok for local testing)
3. Call the number and verify the flow works
4. Measure latency (target: <500ms end-to-end)

## Sample Code Structure
```
vobiz-voice-ai-platform/
├── src/
│   ├── webhooks/
│   │   └── vobiz_handler.py      # Handle incoming call events
│   ├── ai/
│   │   ├── stt_service.py        # Speech-to-Text integration
│   │   ├── llm_engine.py         # LLM conversation logic
│   │   └── tts_service.py        # Text-to-Speech integration
│   ├── telephony/
│   │   └── vobiz_client.py       # Vobiz API wrapper
│   └── main.py                   # FastAPI app entry point
├── tests/
├── .env                          # Store API keys securely
└── requirements.txt
```

## Environment Variables (.env)
```bash
VOBIZ_API_KEY=your_api_key_here
VOBIZ_SIP_SERVER=sip.vobiz.ai
VOBIZ_SIP_USERNAME=your_sip_username
VOBIZ_SIP_PASSWORD=your_sip_password
STT_API_KEY=deepgram_or_whisper_key
LLM_API_KEY=openai_or_anthropic_key
TTS_API_KEY=elevenlabs_key
DATABASE_URL=postgresql://user:pass@localhost:5432/vobiz_voice
```

## Next Steps After Integration
1. Build conversation state management
2. Add voice personality customization
3. Create analytics dashboard
4. Implement call recording (with consent)
5. Add multi-language support

## Resources
- Vobiz API Docs: Check their developer portal after signup
- SIP Protocol Basics: Understand SIP for debugging
- WebRTC: For browser-based calling features

---

**Pro Tip**: Start with a simple "hello world" call flow before building complex conversations. Get the basic pipeline working first!
