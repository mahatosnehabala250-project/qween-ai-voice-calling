# 🦎 n8n Workflows for Voice AI Platform

## Architecture Overview

n8n handles **Post-Call Operations** and **Business Automation**, NOT real-time voice processing.

```
[Live Call] → Python/FastAPI → Gemini 2.5 Live → Supabase
                      ↓
              (Webhook Trigger)
                      ↓
                 [n8n Server]
                      ↓
    ┌─────────────────┼─────────────────┐
    ↓                 ↓                 ↓
[CRM Update]   [SMS/WhatsApp]   [Calendar Booking]
```

## Workflow Catalog

### 1. Post-Call Processing (`post-call-processing.json`)
**Trigger:** Webhook from call agent after call ends
**Actions:**
- Transcribe & summarize call
- Extract intent (booking, inquiry, complaint)
- Update Supabase with call metadata
- Send summary to clinic dashboard
- Trigger follow-up if needed

### 2. Appointment Booking (`appointment-booking.json`)
**Trigger:** Webhook with booking details from AI agent
**Actions:**
- Validate time slot availability
- Create event in Google Calendar/Cal.com
- Send confirmation SMS/WhatsApp via Twilio/Meta API
- Add lead to CRM (HubSpot/Zoho)
- Update Supabase bookings table

### 3. Missed Call Recovery (`missed-call-recovery.json`)
**Trigger:** Supabase new record (missed_call = true)
**Actions:**
- Wait 2 minutes
- Send personalized SMS: "Sorry we missed you! How can we help?"
- If no response in 30 mins → Send WhatsApp
- Log engagement in analytics

### 4. Daily Analytics Report (`daily-analytics.json`)
**Trigger:** Cron (Every day at 9 AM IST)
**Actions:**
- Query Supabase for yesterday's calls
- Calculate metrics: total calls, bookings, recovery rate
- Generate PDF report
- Email to clinic owner
- Post summary to Slack channel

### 5. Patient Reminder (`appointment-reminder.json`)
**Trigger:** Cron (Every hour)
**Actions:**
- Query upcoming appointments (next 24 hours)
- Send reminder SMS/WhatsApp
- Handle confirmations/cancellations via webhook
- Update appointment status

### 6. Lead Qualification Scoring (`lead-scoring.json`)
**Trigger:** Webhook with call transcript
**Actions:**
- Analyze sentiment & intent
- Score lead (Hot/Warm/Cold)
- Assign priority in CRM
- Notify sales team if Hot lead

## Setup Instructions

### Prerequisites
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=<secure_password> \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n:latest
```

### Environment Variables
```env
N8N_HOST=your-domain.com
N8N_PORT=5678
N8N_PROTOCOL=https
WEBHOOK_URL=https://your-domain.com/webhook/
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your_service_role_key
GOOGLE_CALENDAR_CREDENTIALS=encrypted_json
TWILIO_SID=ACxxxx
TWILIO_TOKEN=xxxx
```

### Integration Nodes Used
- **Webhook:** Receive data from voice agent
- **Supabase:** Read/write call data
- **HTTP Request:** Call external APIs
- **Google Calendar:** Book appointments
- **Twilio/WhatsApp:** Send messages
- **Cron:** Schedule reminders/reports
- **Switch/If:** Conditional logic
- **Function Item:** Custom JS transformations

## Security Best Practices
1. Use n8n credentials encryption
2. Restrict webhook URLs with signatures
3. Enable basic auth for n8n UI
4. Use service role keys only server-side
5. Implement rate limiting on webhooks

## Monitoring
- Track workflow execution times
- Set up error alerts (Slack/Email)
- Monitor failed executions daily
- Log all API calls for compliance

## Cost Optimization
- Self-host n8n (free up to 10K executions/month)
- Use efficient queries (filter early)
- Batch operations where possible
- Cache frequently accessed data
