# 🚂 RAILWAY DEPLOYMENT - STEP BY STEP GUIDE

## ✅ PROBLEM FIXED!

**Issue:** Railway was using Python 3.10 but your code needs Python 3.12  
**Solution:** Updated Dockerfile to `python:3.12-slim` ✅  
**Status:** Code pushed to GitHub - Ready for redeploy!

---

## 📋 DEPLOYMENT STEPS (FOLLOW EXACTLY)

### Step 1: Go to Railway Dashboard
👉 https://railway.app/dashboard

### Step 2: Find Your Project
- Look for `qween-ai-voice-calling` project
- If you already deployed and it failed, **DELETE IT** and create new one

### Step 3: Create New Project from GitHub
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose repository: `mahatosnehabala250-project/qween-ai-voice-calling`
4. Railway will auto-detect the **Dockerfile** ✅

### Step 4: Add Environment Variables (CRITICAL!)
In Railway Dashboard → **Project Settings** → **Variables** → Click **"Add Variable"**

Add ALL of these (copy-paste exactly):

```bash
LIVEKIT_URL=wss://queen-voice-calling-1mg10g8y.livekit.cloud
LIVEKIT_API_KEY=APISmFazchqMeSL
LIVEKIT_API_SECRET=PCOvmlE2IVoNhnBA2bP7dOyGgY7PGV3eOUxjvXsaLmL
GEMINI_API_KEY=AIzaSyDwDKqhGfZkLgGm090SN11tI1Uh3j_qSHs
SUPABASE_URL=https://qgybxpteqzhcvlgdfxbn.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR6bGFnaHFqZXRna2Z1Ym1heW9jIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NjU0ODUzMCwiZXhwIjoyMDkyMTI0NTMwfQ.VEavQhoYLD40QD5OsowMXoCipBWfA_txc7zDdS3PKE4
VOBIZ_AUTH_ID=MA_GU1ZOXC3
VOBIZ_AUTH_TOKEN=3wpgv3hIsiylox3J2xuBkcDEzjYoq6W6fMFFvy2cNvuVkYZEMuSln2dYXrxfpzuB
CLINIC_NAME="Queen Voice Dental Clinic"
PORT=8000
PYTHONUNBUFFERED=1
```

⚠️ **IMPORTANT:** Make sure there are NO spaces before/after the values!

### Step 5: Deploy!
1. Go back to **Deployment** tab
2. Click **"Deploy"** (or it may auto-deploy after adding variables)
3. Wait 2-5 minutes for build

---

## ✅ EXPECTED BUILD LOGS

You should see:
```
✅ Building from Dockerfile
✅ Using Python 3.12-slim
✅ Installing requirements.txt
✅ Installing livekit-agents...
✅ Installing google-genai...
✅ Installing mcp...
✅ Build successful
✅ Starting worker...
✅ Worker registered, waiting for jobs...
✅ Health check passed: /health
✅ Service is live!
```

---

## ❌ IF YOU SEE ERRORS

### Error: "Script start.sh not found"
**FIX:** Make sure `railway.json` exists in root (it does ✅)

### Error: "ModuleNotFoundError: No module named 'livekit'"
**FIX:** Check if `requirements.txt` is in root directory (it is ✅)

### Error: "Health check failed"
**FIX:** 
1. Check logs for Python errors
2. Verify all environment variables are set correctly
3. Wait 2 more minutes (sometimes startup is slow)

### Error: "Port not assigned"
**FIX:** Railway auto-assigns ports. Don't worry about PORT variable.

---

## 🧪 TEST AFTER SUCCESSFUL DEPLOY

### 1. Check Logs
In Railway Dashboard → **Deployments** → Click on your deployment → **View Logs**

Look for:
```
Worker registered, waiting for jobs...
```

### 2. Configure Vobiz SIP
1. Go to https://vobiz.ai/
2. Navigate to **SIP Trunks** → **Inbound**
3. Set destination to: `sip:1bjaxvvkfgg.sip.livekit.cloud`
4. Save & Enable

### 3. Configure LiveKit Dispatch Rule
1. Go to https://cloud.livekit.io/projects/p_1bjaxvvkfgg
2. Navigate to **SIP** → **Dispatch Rules**
3. Create rule: Route all calls → room `queen-agent`

### 4. MAKE TEST CALL! 📞
Dial **+91 80654 81672**

You should hear:
> *"Namaste! Main Dr. Priya bol rahi hoon, Queen Voice Dental Clinic se. Main aapki kaise madad kar sakti hoon?"*

---

## 💰 COST ESTIMATE

Railway Hobby Plan: **$5/month** (or free tier if available)  
+ Vobiz: ₹0.67/min  
+ Gemini: ₹0.06/min  
+ Supabase: Free tier  

**Total fixed cost:** ~₹450/month  
**Variable cost:** ₹0.73/min per call

---

## 🎯 NEXT STEPS AFTER DEPLOYMENT

1. ✅ Deploy on Railway (follow this guide)
2. ✅ Make first test call
3. ✅ Test Hindi + English conversations
4. ✅ Test appointment booking flow
5. ✅ Demo to 3 dental clinics tomorrow!

---

## 🆘 NEED HELP?

If deployment still fails:
1. Take screenshot of error logs
2. Check all environment variables again
3. Make sure GitHub repo is public or Railway has access
4. Try deleting project and creating fresh one

**Your code is correct. The fix has been pushed. Now deploy!** 🚀

Jai Hind! 🇮🇳
