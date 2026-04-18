# 🚀 QUEEN VOICE - DEPLOYMENT CHECKLIST

## ✅ FRONTEND (Vercel) - READY TO DEPLOY!

### Files Created:
- `frontend/package.json` - Next.js 14 configuration
- `frontend/src/app/page.js` - Landing page with demo call button
- `frontend/src/app/layout.js` - Root layout
- `frontend/next.config.js` - Next.js config
- `frontend/tailwind.config.js` - Tailwind CSS config
- `frontend/.gitignore` - Git ignore rules

### Deploy to Vercel (5 minutes):

1. **Go to https://vercel.com**
2. Click **"Add New Project"**
3. Import GitHub repo: `mahatosnehabala250-project/qween-ai-voice-calling`
4. **Framework Preset:** Next.js (auto-detected)
5. **Root Directory:** `frontend`
6. **Environment Variables:**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.railway.app
   ```
7. Click **"Deploy"**

🎉 **Live URL:** `https://queen-voice-calling.vercel.app`

---

## ⚠️ BACKEND (Python/LiveKit) - CANNOT Deploy to Vercel!

**You need Railway, Render, or Fly.io for the Python agent.**

### Option A: Railway (Recommended - 5 minutes)

1. Go to https://railway.app
2. Click **"New Project"** → **"Deploy from GitHub"**
3. Select repo: `qween-ai-voice-calling`
4. **Add Environment Variables:**
   ```bash
   LIVEKIT_URL=wss://queen-voice-calling-1mg10g8y.livekit.cloud
   LIVEKIT_API_KEY=APISmFazchqMeSL
   LIVEKIT_API_SECRET=PCOvmlE2IVoNhnBA2bP7dOyGgY7PGV3eOUxjvXsaLmL
   GEMINI_API_KEY=AIzaSyDwDKqhGfZkLgGm090SN11tI1Uh3j_qSHs
   SUPABASE_URL=https://qgybxpteqzhcvlgdfxbn.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (use anon key from .env)
   CLINIC_NAME="Queen Voice Clinic"
   VOICE_NAME="Kore"
   ```
5. **Deploy!**
   
🎉 **Backend URL:** `https://queen-voice-production.up.railway.app`

### Option B: Render (Alternative)

1. Go to https://render.com
2. **New Web Service** → Connect GitHub
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `python -m uvicorn src.main:app --host 0.0.0.0 --port $PORT`
5. Add same environment variables as above

---

## 🔧 POST-DEPLOYMENT CONFIGURATION

### 1. Configure Vobiz SIP Trunk

1. Login to https://vobiz.ai/
2. Go to **SIP Trunks** → **Inbound**
3. Set destination URI: `sip:1bjaxvvkfgg.sip.livekit.cloud`
4. Save & Enable

### 2. Configure LiveKit Dispatch Rule

1. Go to https://cloud.livekit.io/projects/p_1bjaxvvkfgg
2. Navigate to **SIP** → **Dispatch Rules**
3. Create rule:
   - **Trunk:** Vobiz inbound
   - **Room Prefix:** `queen-agent`
   - **Agent:** Your LiveKit agent
4. Save

### 3. Test the System

1. Call **+91 80654 81672** from your phone
2. You should hear: *"Namaste! Main Queen bol rahi hoon..."*
3. Speak in Hindi or English
4. Test appointment booking

---

## 💰 COST BREAKDOWN

| Service | Plan | Monthly Cost |
|---------|------|--------------|
| **Vercel** | Hobby | FREE |
| **Railway** | Starter | $5 (~₹415) |
| **LiveKit Cloud** | Pay-as-you-go | ~$10-20 usage |
| **Supabase** | Free Tier | FREE |
| **Vobiz** | Per minute | ₹0.67/min |
| **Gemini API** | Per token | ₹0.06/min |

**Total Fixed:** ~₹500/month  
**Variable:** ₹0.73/min of calls

---

## 🎯 SUCCESS METRICS

After deployment, track:
- ✅ First successful call
- ✅ Appointment booked via AI
- ✅ <600ms latency
- ✅ 98%+ answer rate
- ✅ First paying customer

---

## 🚨 COMMON ERRORS & FIXES

### Vercel Error: "Build failed"
**Fix:** Check logs. Usually missing `next.config.js` or wrong Node version (use 18.x)

### Vercel Error: "Module not found"
**Fix:** Run `npm install` locally, commit `package-lock.json`, push again

### Backend Not Connecting to LiveKit
**Fix:** 
1. Verify env vars match exactly
2. Check LiveKit project is active
3. Ensure dispatch rules configured

### Call Not Routing
**Fix:**
1. Verify Vobiz SIP URI points to LiveKit
2. Check LiveKit dispatch rules
3. Ensure agent worker is running

---

## 📞 NEXT STEPS (This Week)

| Day | Task | Goal |
|-----|------|------|
| **Today** | Deploy frontend to Vercel | ✅ Website live |
| **Tomorrow** | Deploy backend to Railway | ✅ API running |
| **Day 3** | Configure Vobiz + LiveKit | ✅ Calls routing |
| **Day 4** | Test end-to-end | ✅ First call works |
| **Day 5** | Demo to 3 dental clinics | 🎯 Get feedback |
| **Weekend** | Iterate based on feedback | 🚀 Close first pilot |

---

## 🇮🇳 YOU'RE READY!

**Sab kuch ready hai:**
- ✅ Frontend code (Vercel-ready)
- ✅ Backend code (Railway-ready)
- ✅ Credentials configured
- ✅ Documentation complete

**Ab bas deploy karo aur paisa kamayo!**

**Jai Hind! 🚀**
