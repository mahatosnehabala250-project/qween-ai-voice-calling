# 🚀 START HERE - Your 7-Day MVP Launch Plan

**Welcome to Vobiz Voice AI Platform!**  
This is your complete guide to launching a voice AI business for Indian dental clinics in 7 days.

---

## 📅 DAY-BY-DAY PLAN

### **DAY 1: Setup Accounts & Environment (4 hours)**

#### ✅ Create These Accounts:
1. **Vobiz** - https://vobiz.ai/
   - Get API key, SIP credentials
   - Note: May need to contact sales for access

2. **Google Cloud** - https://console.cloud.google.com/
   - Enable Gemini API
   - Get API key for `gemini-2.5-flash-preview-05-20`
   - Set billing (₹300 free credit)

3. **Supabase** - https://supabase.com/
   - Create project in **Mumbai region** (asia-south-1)
   - Get URL and anon/service keys

4. **n8n** - Will self-host via Docker (free!)

#### ✅ Clone & Configure:
```bash
cd /workspace/vobiz-voice-ai
cp .env.example .env
```

Edit `.env` with your actual API keys:
- `VOBIZ_API_KEY`, `VOBIZ_SIP_USERNAME`, `VOBIZ_SIP_PASSWORD`
- `GOOGLE_API_KEY`
- `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`

---

### **DAY 2: Local Development Setup (6 hours)**

#### ✅ Install Dependencies:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### ✅ Start Infrastructure:
```bash
cd docker
docker-compose up -d supabase-db redis n8n
```

Verify services running:
- PostgreSQL: http://localhost:5432
- Redis: http://localhost:6379
- n8n: http://localhost:5678

#### ✅ Run the App:
```bash
cd ..
python -m uvicorn src.main:app --reload
```

Visit: http://localhost:8000/docs

You should see FastAPI Swagger UI! 🎉

---

### **DAY 3: Database & First Test Call (8 hours)**

#### ✅ Initialize Database:
```bash
docker exec -i <postgres_container_id> psql -U postgres -d vobiz_voice_ai < docker/init.sql
```

Check tables created:
```sql
SELECT * FROM businesses;
SELECT * FROM agent_configs;
```

#### ✅ Import n8n Workflow:
1. Open http://localhost:5678
2. Go to Settings → Workflows → Import
3. Select `workflows/post-call-processing.json`
4. Activate the workflow

#### ✅ Make Your First Test Call:
Use this curl command to simulate a call:
```bash
curl -X POST http://localhost:8000/api/v1/calls/start \
  -H "Content-Type: application/json" \
  -d '{
    "business_id": "<get-from-database>",
    "caller_phone": "+919876543210",
    "call_direction": "inbound"
  }'
```

---

### **DAY 4: Integrate Real Telephony (8 hours)**

#### ✅ Connect Vobiz Webhook:
In Vobiz dashboard, set webhook URL to:
```
https://your-ngrok-url.ngrok.io/api/v1/webhooks/vobiz
```

Use ngrok for local testing:
```bash
ngrok http 8000
```

#### ✅ Test End-to-End Flow:
1. Call your Vobiz number
2. Verify webhook hits your server
3. Check logs for processing
4. Verify data saved to Supabase
5. Check n8n workflow triggered

---

### **DAY 5: Build Dental Clinic Agent (8 hours)**

Create `src/agents/dental_assistant.py`:

```python
"""
Dr. Priya - Dental Assistant Agent
Speaks English + Hindi
"""

SYSTEM_PROMPT = """
You are Dr. Priya, a friendly dental assistant at Smile Care Dental Clinic.

YOUR ROLE:
1. Answer patient questions about dental services
2. Book appointments based on available slots
3. Handle emergencies by escalating to human staff
4. Provide pricing information for common procedures

LANGUAGES: Speak both English and Hindi fluently. Match the caller's language.

PERSONALITY: Warm, professional, empathetic. Never rush the caller.

ESCALATION RULES:
- Severe pain → Immediately transfer to human
- Complex treatment questions → Transfer to doctor
- Payment disputes → Transfer to receptionist

AVAILABLE SERVICES:
- General Checkup: ₹500
- Cleaning: ₹1,500
- Root Canal: ₹3,000-5,000
- Extraction: ₹800-2,000
- Implants: ₹15,000+

BUSINESS HOURS: Mon-Sat 9AM-7PM, Sunday Closed
EMERGENCY CONTACT: +91-9876543210
"""
```

Test with sample conversations in Hindi and English!

---

### **DAY 6: Pilot Customer Onboarding (8 hours)**

#### ✅ Find Your First Pilot Clinic:
Target: Local dental clinic you know

Pitch Script:
> "Hi Dr. [Name], I'm building an AI receptionist that answers patient calls 24/7 in English and Hindi. It books appointments automatically and never misses a call. I'm looking for 3 pilot clinics to try it free for 2 weeks. Can I demo it for you?"

#### ✅ Demo Checklist:
- [ ] Show live call demo
- [ ] Explain missed call recovery
- [ ] Show WhatsApp confirmations
- [ ] Display ROI dashboard
- [ ] Offer 2-week free trial

Goal: Get 1 clinic to say YES! 🎯

---

### **DAY 7: Deploy to Production (8 hours)**

#### ✅ Deploy on AWS Mumbai:
```bash
# Build Docker image
docker build -t vobiz-voice-ai .

# Push to ECR or Docker Hub
docker push your-username/vobiz-voice-ai

# Deploy on EC2 or ECS
# Use docker-compose.prod.yml for production config
```

#### ✅ Setup Monitoring:
- Add health check alerts
- Monitor latency (<600ms target)
- Track call success rate (>95% target)

#### ✅ Launch Checklist:
- [ ] Domain purchased (e.g., vobiz.in)
- [ ] SSL certificate installed
- [ ] Backup strategy configured
- [ ] Support email setup (support@vobiz.in)
- [ ] First paying customer onboarded!

---

## 💰 PRICING TO CHARGE FROM DAY 1

Don't give it away free forever! Charge from Week 2:

| Plan | Price | What's Included |
|------|-------|-----------------|
| **Pilot** | FREE (2 weeks) | 500 mins, basic features |
| **Startup** | ₹2,499/mo | 500 mins, WhatsApp, calendar |
| **Business** | ₹7,999/mo | 2,500 mins, analytics, priority support |

**Goal:** Convert pilot to paid at ₹2,499/month after 2 weeks!

---

## 🎯 SUCCESS METRICS

Track these from Day 1:

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| Latency | <600ms | Natural conversation flow |
| Answer Rate | >95% | Never miss calls |
| Booking Conversion | >15% | Proves ROI to clinics |
| Customer Satisfaction | >4.5/5 | Retention & referrals |
| Margin | >75% | Sustainable business |

---

## 🆘 COMMON ISSUES & FIXES

### Issue: High Latency (>1s)
**Fix:** 
- Use Gemini 2.5 Flash (not Pro)
- Deploy server in Mumbai (closest to users)
- Optimize audio streaming (use websockets)

### Issue: Hindi Not Working Well
**Fix:**
- Set `GEMINI_LANGUAGE_CODE=hi-IN`
- Train agent with Hindi dental terminology
- Add fallback to English if confidence low

### Issue: Vobiz Webhook Not Received
**Fix:**
- Check ngrok is running
- Verify webhook signature validation
- Check firewall allows inbound connections

### Issue: n8n Workflow Failing
**Fix:**
- Check webhook URL is correct
- Verify Supabase credentials
- Look at n8n execution logs

---

## 📞 NEED HELP?

Resources:
- FastAPI Docs: https://fastapi.tiangolo.com/
- Gemini API: https://ai.google.dev/
- Vobiz Docs: https://vobiz.ai/docs
- n8n Workflows: https://n8n.io/workflows

Community:
- Join Indian startup Discord servers
- Post on LinkedIn (#VoiceAI #IndiaStartups)
- Reach out to dental associations

---

## 🚀 AFTER 7 DAYS: WHAT'S NEXT?

### Week 2-3:
- Onboard 2 more pilot clinics
- Integrate with popular calendar systems (Google Calendar, Practo)
- Build admin dashboard for clinics

### Week 4:
- Start charging all pilots
- Get testimonials & case studies
- Build landing page with pricing

### Month 2:
- Hire first sales person
- Target 10 more clinics
- Explore adjacent verticals (veterinary, salons)

### Month 3:
- Raise pre-seed funding (if needed)
- Expand to 5 cities
- Hit ₹1 Lakh MRR!

---

## 🎓 MENTOR'S FINAL ADVICE

> **"Your biggest risk is not launching. Perfection is the enemy of done.**
>
> **Day 1: Setup accounts**
> **Day 3: Make first test call**
> **Day 7: Get first paying customer**
>
> **Don't over-engineer. Don't wait for perfect. Just SHIP!**
>
> **Indian healthcare needs this. Patients deserve 24/7 access. You're building something meaningful.**
>
> **Jai Hind! 🇮🇳 Now go execute!"**

---

**Ready? Let's build the future of Indian healthcare together!** 🦷🤖
