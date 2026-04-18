# LiveKit + Vobiz Integration Guide

Complete setup for connecting Vobiz SIP trunk to LiveKit Agents with Gemini 2.5 Flash Live.

## Architecture

```
Customer Call → Vobiz SIP Trunk → LiveKit Server → Gemini 2.5 Flash Live Agent → n8n Workflows
```

## Prerequisites

1. **Vobiz Account**: https://vobiz.ai/
   - Create SIP Trunk
   - Get credentials: SIP Username, Password, Server

2. **Google Cloud Account**: 
   - Enable Vertex AI API
   - Get API Key for Gemini 2.5 Flash

3. **LiveKit Cloud** (or self-hosted):
   - Sign up at https://cloud.livekit.io/
   - Get Project URL, API Key, Secret

4. **n8n Instance**:
   - Self-hosted or cloud
   - Base URL and API key

## Step 1: Install Dependencies

```bash
pip install livekit livekit-agents livekit-plugins-google livekit-plugins-deepgram livekit-plugins-silero mcp
```

## Step 2: Configure Environment Variables

Create `.env` file:

```bash
# Vobiz SIP Configuration
VOBIZ_SIP_SERVER=sip.vobiz.ai
VOBIZ_SIP_USERNAME=your_trunk_username
VOBIZ_SIP_PASSWORD=your_trunk_password
VOBIZ_PHONE_NUMBER=+91XXXXXXXXXX

# LiveKit Configuration
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret

# Google Gemini Configuration
GOOGLE_API_KEY=your_google_api_key
GEMINI_MODEL=gemini-2.5-flash-preview-native-audio-dialog

# n8n Configuration
N8N_BASE_URL=https://your-n8n-instance.com
N8N_API_KEY=your_n8n_api_key

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key
```

## Step 3: Deploy LiveKit Server

### Option A: LiveKit Cloud (Recommended)

1. Go to https://cloud.livekit.io/
2. Create new project
3. Copy credentials to `.env`
4. Done! No server management needed

### Option B: Self-Hosted with Docker

```bash
docker run --rm \
  -p 7880:7880 \
  -e LIVEKIT_KEYS="devkey: secret" \
  livekit/livekit-server --dev
```

## Step 4: Configure Vobiz SIP Trunk

1. Login to Vobiz Dashboard
2. Go to **Trunks** → **Create New Trunk**
3. Configure:
   - **Name**: Dental Clinic AI
   - **Type**: SIP Trunk
   - **Destination**: LiveKit SIP URI
   - **Codecs**: OPUS, PCMU, PCMA
4. Get SIP credentials

### Vobiz Dispatch Rules

Configure dispatch rule to route calls to LiveKit:

```json
{
  "room_name": "clinic-{caller_number}",
  "agents": ["voice-assistant"],
  "metadata": {
    "clinic_id": "dental-clinic-001",
    "language": "hi"
  }
}
```

## Step 5: Run the Agent

```bash
cd /workspace/vobiz-voice-ai

# Activate virtual environment
source venv/bin/activate

# Run LiveKit agent
python -m src.livekit_agent
```

## Step 6: Test the Integration

### Make a Test Call

1. Dial your Vobiz phone number
2. Agent should answer with: "Namaste! Main Dr. Priya bol rahi hoon..."
3. Test conversation in Hindi/English
4. Try booking an appointment

### Expected Flow

```
Caller: "Hello, I need a dental checkup"
Agent: "Namaste! I'd be happy to help. May I have your name please?"
Caller: "Rajesh Kumar"
Agent: "Thank you Rajesh. What date and time works for you?"
Caller: "Tomorrow at 3 PM"
Agent: [Calls book_appointment function]
       "Appointment booked for tomorrow at 3 PM. You'll receive WhatsApp confirmation!"
```

## Step 7: Monitor & Debug

### Check LiveKit Dashboard

- View active rooms
- Monitor participant connections
- Check audio quality metrics

### Check Logs

```bash
# Agent logs
tail -f logs/agent.log

# n8n workflow executions
Visit: https://your-n8n-instance.com/executions
```

## Troubleshooting

### Issue: Agent doesn't answer calls

**Solution:**
- Verify Vobiz dispatch rules point to LiveKit
- Check LiveKit worker is running
- Ensure SIP credentials are correct

### Issue: High latency (>1 second)

**Solution:**
- Use LiveKit Cloud (edge locations)
- Reduce Gemini model complexity
- Check network connectivity

### Issue: Hindi not recognized properly

**Solution:**
- Explicitly set language in STT config
- Train persona with more Hindi examples
- Use Hinglish (Hindi+English mix) in prompts

### Issue: MCP tools not working

**Solution:**
- Verify MCP server is installed: `pip install mcp-server-calendar`
- Check GOOGLE_API_KEY is set
- Review MCP initialization logs

## Cost Breakdown (per minute)

| Component | Cost (INR) |
|-----------|------------|
| Vobiz SIP | ₹0.67 |
| Gemini 2.5 Live | ₹0.06 |
| LiveKit | FREE (first 1,000 min/month) |
| n8n | FREE (self-hosted) |
| **Total** | **₹0.73/min** |

## Next Steps

1. ✅ Test with single clinic
2. ✅ Refine Dr. Priya persona
3. ✅ Integrate Google Calendar via MCP
4. ✅ Add WhatsApp confirmations via n8n
5. ✅ Scale to 10 clinics
6. ✅ Build analytics dashboard

## Resources

- LiveKit Docs: https://docs.livekit.io/
- LiveKit + Vobiz: https://www.docs.vobiz.ai/integrations/livekit
- Gemini API: https://ai.google.dev/gemini-api/docs
- MCP Protocol: https://docs.livekit.io/agents/logic/tools/mcp/
- n8n Workflows: https://n8n.io/workflows/

## Support

For issues:
- LiveKit Discord: https://livekit.io/discord
- Vobiz Support: support@vobiz.ai
- GitHub Issues: /workspace/vobiz-voice-ai/issues
