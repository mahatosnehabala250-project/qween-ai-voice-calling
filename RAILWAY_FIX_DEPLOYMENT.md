# 🚨 RAILWAY DEPLOYMENT FIX - LIVEKIT AGENT

## ❌ PROBLEM DIAGNOSED

Railway ne error diya: **"Script start.sh not found"** aur **"Railpack could not determine how to build"**

**Reason:** Railway ka naya "Railpack" system automatically detect karta hai language, lekin:
1. Root directory mein `requirements.txt` nahi tha (wo `vobiz-voice-ai/` folder mein tha)
2. `Dockerfile` bhi root mein nahi tha
3. Railway ko direct Python project dikha nahi

---

## ✅ SOLUTION: MOVE FILES TO ROOT

Tumhare code ko properly structure karna padega taki Railway Dockerfile use kar sake.

### Step 1: Move All Files to Root Directory

Abhi structure ye hai:
```
/workspace/
├── vobiz-voice-ai/      ← Sab kuch isme hai
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── railway.json
│   └── src/
├── MASTER_PLAN.md
└── ...other docs
```

**Change to:**
```
/workspace/
├── Dockerfile           ← Root pe lao
├── requirements.txt     ← Root pe lao
├── railway.json         ← Root pe lao
├── .env.example         ← Root pe lao
├── src/                 ← Root pe lao
├── docker/
├── workflows/
├── frontend/            ← Separate Vercel deploy ke liye
└── docs/                ← Baaki docs move karo
```

---

## 🔧 EXECUTE THESE COMMANDS NOW:

```bash
cd /workspace

# 1. Move critical files to root
mv vobiz-voice-ai/Dockerfile .
mv vobiz-voice-ai/requirements.txt .
mv vobiz-voice-ai/railway.json .
mv vobiz-voice-ai/.env.example .
mv vobiz-voice-ai/src .
mv vobiz-voice-ai/docker .
mv vobiz-voice-ai/workflows .
mv vobiz-voice-ai/tests .

# 2. Move docs to separate folder (optional, for cleanliness)
mkdir -p docs-archive
mv *.md docs-archive/ 2>/dev/null || true
mv vobiz-voice-ai/*.md . 2>/dev/null || true

# 3. Verify structure
ls -la
```

---

## 📝 UPDATE .gitignore (Important!)

`.env` file ko commit mat karna! Add to `.gitignore`:

```bash
cat > .gitignore << EOF
# Environment
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db

# Frontend (separate repo)
frontend/node_modules/
frontend/.next/

# Test
.pytest_cache/
.coverage
htmlcov/
EOF
```

---

## 🚂 RAILWAY SETUP STEPS:

### 1. Push to GitHub
```bash
cd /workspace
git add -A
git commit -m "fix: Move all files to root for Railway deployment"
git push origin main
```

### 2. Railway Pe Deploy
1. **Go to:** https://railway.app/dashboard
2. **Click:** "New Project" → "Deploy from GitHub repo"
3. **Select:** `qween-ai-voice-calling`
4. **Railway will auto-detect:** Dockerfile ✅
5. **Click Deploy!**

### 3. Add Environment Variables in Railway Dashboard

Project Settings → Variables → Add ALL of these:

```env
# LiveKit
LIVEKIT_URL=wss://queen-voice-calling-1mg10g8y.livekit.cloud
LIVEKIT_API_KEY=APISmFazchqMeSL
LIVEKIT_API_SECRET=PCOvmlE2IVoNhnBA2bP7dOyGgY7PGV3eOUxjvXsaLmL

# Google Gemini
GEMINI_API_KEY=AIzaSyDwDKqhGfZkLgGm090SN11tI1Uh3j_qSHs

# Supabase
SUPABASE_URL=https://qgybxpteqzhcvlgdfxbn.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR6bGFnaHFqZXRna2Z1Ym1heW9jIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzY1NDg1MzAsImV4cCI6MjA5MjEyNDUzMH0.t-pG8OPl0MoZaZdPqfj7b23DjcViw96Hr6yZ6GF3Nb4
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR6bGFnaHFqZXRna2Z1Ym1heW9jIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NjU0ODUzMCwiZXhwIjoyMDkyMTI0NTMwfQ.VEavQhoYLD40QD5OsowMXoCipBWfA_txc7zDdS3PKE4

# Vobiz
VOBIZ_AUTH_ID=MA_GU1ZOXC3
VOBIZ_AUTH_TOKEN=3wpgv3hIsiylox3J2xuBkcDEzjYoq6W6fMFFvy2cNvuVkYZEMuSln2dYXrxfpzuB
VOBIZ_PHONE=+918065481672

# App Config
CLINIC_NAME="Queen Voice Dental Clinic"
PORT=8000
PYTHONUNBUFFERED=1
```

---

## ✅ VERIFICATION CHECKLIST

After deployment starts:

1. **Build Log Check:**
   - ✅ "Building from Dockerfile"
   - ✅ "Installing requirements.txt"
   - ✅ "Copy application code"
   - ✅ "Build successful"

2. **Deploy Log Check:**
   - ✅ "Starting worker..."
   - ✅ "Worker registered, waiting for jobs..."
   - ✅ Health check passed: `/health`

3. **Test Call:**
   - Dial **+91 80654 81672**
   - Hear: *"Namaste! Main Dr. Priya bol rahi hoon..."*

---

## 🎯 ALTERNATIVE: USE DOCKER DEPLOY DIRECTLY

Agar Railway se issue ho, to directly Docker use karo:

### Option A: Render.com (FREE Tier)
1. https://render.com → New Web Service
2. Connect GitHub repo
3. Build Command: `docker build -t queen-voice .`
4. Start Command: `python -m src.livekit_agent_mcp start`
5. Add environment variables

### Option B: Fly.io
```bash
flyctl launch --dockerfile ./Dockerfile
flyctl secrets set LIVEKIT_URL=... GEMINI_API_KEY=...
flyctl deploy
```

### Option C: Hugging Face Spaces (Docker)
1. Create Space → Select "Docker"
2. Push code to space
3. Add secrets in settings

---

## 💡 WHY THIS HAPPENED

Railway's new "Railpack" system tries to auto-detect your app type:
- It saw `.md` files → Confused
- It didn't find `requirements.txt` in root → Thought no Python
- It looked for `start.sh` → Not found

**Solution:** Dockerfile explicitly batata hai ki kya karna hai → No confusion!

---

## 🚀 NEXT STEPS AFTER DEPLOYMENT

1. **Configure Vobiz SIP Trunk:**
   - Vobiz Dashboard → SIP → Inbound
   - Destination: `sip:1bjaxvvkfgg.sip.livekit.cloud`

2. **Configure LiveKit Dispatch Rule:**
   - LiveKit Cloud → SIP → Dispatch Rules
   - Route calls to room: `queen-agent`

3. **Test Call:** +91 80654 81672

4. **Demo to Clinics:** Start calling dental clinics tomorrow!

---

## 📞 SUPPORT

Agar abhi bhi error aaye:
1. Railway build logs check karo
2. Error message copy karo
3. Railway Discord ya support ticket raise karo

**You're 10 minutes away from your first AI call! 🎉**

Jai Hind! 🇮🇳
