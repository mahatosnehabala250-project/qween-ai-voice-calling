# 🦷 Vobiz Voice AI Platform

**AI-powered voice calling for Indian Dental Clinics**  
*Never miss a patient call. Book more revenue.*

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Accounts: [Vobiz](https://vobiz.ai/), Google Cloud, Supabase

### 1. Clone & Setup
```bash
cd vobiz-voice-ai
cp .env.example .env
# Edit .env with your API keys
```

### 2. Start Services
```bash
docker-compose up -d supabase-db redis n8n
pip install -r requirements.txt
```

### 3. Run Development Server
```bash
python -m uvicorn src.main:app --reload
```

Visit: http://localhost:8000/docs

---

## 🏗️ Architecture

```
Patient Call → Vobiz (Telephony) → FastAPI Server → Gemini 2.5 Live (STT+LLM+TTS)
                                              ↓
Supabase (DB) ← Post-Call Data → n8n (WhatsApp/Slack/CRM Automation)
```

### Tech Stack
| Component | Technology | Cost/min (INR) |
|-----------|------------|----------------|
| Telephony | Vobiz | ₹0.67 |
| Voice AI | Gemini 2.5 Flash Live | ₹0.06 |
| Database | Supabase Mumbai | ₹0.08 |
| Automation | n8n (self-hosted) | FREE |
| **TOTAL** | | **₹0.81/min** |

---

## 📁 Project Structure

```
vobiz-voice-ai/
├── src/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Environment configuration
│   ├── routes/
│   │   ├── calls.py         # Call management endpoints
│   │   ├── webhooks.py      # Vobiz/n8n webhooks
│   │   └── analytics.py     # Analytics & ROI
│   ├── agents/              # Gemini AI agent logic
│   ├── integrations/        # Vobiz, Supabase, n8n clients
│   └── utils/               # Helpers & utilities
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── init.sql             # Database schema
├── workflows/
│   └── post-call-processing.json  # n8n workflow
├── .env.example
├── requirements.txt
└── README.md
```

---

## 💼 Business Model (India)

### Target Market: Dental Clinics
- **Problem:** Missed calls = lost patients (₹3,000-10,000 per procedure)
- **Solution:** 24/7 AI receptionist in English + Hindi

### Pricing Plans
| Plan | Price/Mo | Minutes | Target |
|------|----------|---------|--------|
| Startup | ₹2,499 | 500 | Small clinics |
| Business | ₹7,999 | 2,500 | Multi-doctor clinics |
| Enterprise | ₹25,000+ | 10,000+ | Hospital chains |

### Unit Economics (Business Plan)
- Revenue: ₹7,999/month
- Costs: ₹2,025/month (2,500 min × ₹0.81)
- **Profit: ₹5,974/month (75% margin)**

---

## 🔑 Key Features

✅ **Missed Call Recovery** - Answer 24/7, even after hours  
✅ **Appointment Booking** - Direct calendar integration  
✅ **Bilingual Support** - English + Hindi (expandable)  
✅ **Smart Escalation** - Transfer to human when needed  
✅ **WhatsApp Confirmations** - Automated via n8n  
✅ **ROI Dashboard** - Show clinics revenue generated  

---

## 📋 Next Steps

### Week 1: MVP
- [ ] Create Vobiz account & get API keys
- [ ] Setup Google Cloud for Gemini 2.5 Live
- [ ] Create Supabase project (Mumbai region)
- [ ] Test first voice call end-to-end

### Week 2-3: Pilot
- [ ] Onboard 3 dental clinics (free pilot)
- [ ] Integrate with their calendars
- [ ] Collect feedback & iterate

### Week 4: Launch
- [ ] Start charging ₹2,499/month
- [ ] Build case studies from pilots
- [ ] Scale to 10 more clinics

---

## 🤝 Contributing

This is a private startup project. For questions, contact the founder.

---

## 📄 License

Proprietary - All rights reserved.

---

**Built with ❤️ for Indian Healthcare**  
*Jai Hind! 🇮🇳*
