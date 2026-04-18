# 🚂 Railway Deployment Guide for Queen Voice AI

Since Vercel only supports static frontends and serverless functions (not long-running WebSocket servers), we must deploy the **LiveKit Agent** on a platform that supports Docker/Python workers.

**Recommended Platform:** [Railway.app](https://railway.app) (Best for LiveKit + Python)
**Alternative:** Render.com or AWS EC2

## 🛠️ Prerequisites
1. GitHub Account (Code already pushed)
2. Railway Account (Free trial available)
3. Docker installed locally (optional, for testing)

---

## 📋 Step 1: Prepare `railway.json` (Already Created)
This file tells Railway how to start your agent.
- **Start Command:** `python -m src.livekit_agent_mcp start`
- **Healthcheck:** `/health` endpoint

## 📋 Step 2: Environment Variables
Copy all variables from your `.env` file to Railway Project Settings > Variables:
- `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`
- `GEMINI_API_KEY`
- `SUPABASE_URL`, `SUPABASE_KEY`
- `VOBIZ_AUTH_ID`, `VOBIZ_AUTH_TOKEN`
- `PORT` (Set to `8000` or let Railway auto-assign)

## 📋 Step 3: Deploy to Railway

### Option A: One-Click Deploy (Easiest)
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"** -> **"Deploy from GitHub repo"**
3. Select repo: `mahatosnehabala250-project/qween-ai-voice-calling`
4. Railway will auto-detect `Dockerfile` and `railway.json`.
5. Click **"Deploy"**.

### Option B: Manual CLI
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

## 📋 Step 4: Configure LiveKit & Vobiz

Once Railway gives you a public URL (e.g., `https://queen-voice-production.up.railway.app`):

### 1. Update LiveKit Dispatch Rule
Go to [LiveKit Cloud](https://cloud.livekit.io/projects/p_1bjaxvvkfgg/sip/dispatch-rules):
- **Trunk:** Vobiz Inbound
- **Room Name:** `queen-agent-room` (or dynamic)
- **Agent URL:** `https://queen-voice-production.up.railway.app` (If using LiveKit Agents Playground)
   *Note: If running as a standalone worker, just ensure the worker connects to LiveKit via WS.*

### 2. Update Vobiz SIP Trunk
Go to [Vobiz Dashboard](https://vobiz.ai/trunks):
- Ensure Inbound SIP URI points to LiveKit: `sip:1bjaxvvkfgg.sip.livekit.cloud`
- LiveKit will then hand off to your Worker running on Railway.

## 🧪 Step 5: Test
1. Wait for Railway build to finish (Green checkmark).
2. Check logs in Railway dashboard for: `Worker registered, waiting for jobs...`
3. Call your Vobiz number: **+91 80654 81672**
4. You should hear: *"Namaste! Main Queen bol rahi hoon..."*

## ⚠️ Troubleshooting
- **Crash Loop:** Check Railway logs for missing Env Vars.
- **Timeout:** Ensure `LIVEKIT_URL` is correct (`wss://...`).
- **404 on Root:** The root `/` might not have a webpage. This is normal. The agent listens on WebSockets. Use `/health` to check status.

---

## 💰 Cost Estimate
- **Railway:** ~$5-10/month for basic usage (Hobby plan).
- **LiveKit:** Free tier sufficient for starting.
- **Vobiz:** Pay per minute.
- **Gemini:** Pay per token (very cheap for voice).

**Total Monthly Infra Cost:** < $20 until you scale!
