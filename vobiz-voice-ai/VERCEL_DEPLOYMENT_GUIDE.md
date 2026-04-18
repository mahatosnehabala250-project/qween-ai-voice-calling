# 🚀 VERCEL DEPLOYMENT GUIDE - QUEEN VOICE CALLING

## ⚠️ IMPORTANT: Vercel Limitations

**Vercel is for FRONTEND only (Next.js/React).**
Your **Voice AI Agent (Python/LiveKit) CANNOT run on Vercel**.

### ✅ Correct Architecture:
```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   VERCEL        │      │   RAILWAY/       │      │   LIVEKIT       │
│   (Frontend)    │─────▶│   RENDER         │─────▶│   (Voice Agent) │
│   Next.js Dashboard│    │   (Python API)   │      │   Cloud         │
└─────────────────┘      └──────────────────┘      └─────────────────┘
                                │
                                ▼
                         ┌──────────────────┐
                         │   SUPABASE       │
                         │   (Database)     │
                         └──────────────────┘
```

---

## 📋 DEPLOYMENT STEPS

### PART 1: Deploy Python Backend (Railway/Render)

**Option A: Railway (Recommended)**
1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repo: `mahatosnehabala250-project/qween-ai-voice-calling`
4. Add Environment Variables (from `.env`):
   ```
   LIVEKIT_URL=wss://queen-voice-calling-1mg10g8y.livekit.cloud
   LIVEKIT_API_KEY=APISmFazchqMeSL
   LIVEKIT_API_SECRET=PCOvmlE2IVoNhnBA2bP7dOyGgY7PGV3eOUxjvXsaLmL
   GEMINI_API_KEY=AIzaSyDwDKqhGfZkLgGm090SN11tI1Uh3j_qSHs
   SUPABASE_URL=https://qgybxpteqzhcvlgdfxbn.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (anon key)
   CLINIC_NAME="Queen Voice Clinic"
   ```
5. Deploy! You'll get a URL like: `https://queen-voice-production.up.railway.app`

**Option B: Render**
1. Go to https://render.com
2. New Web Service → Connect GitHub
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python -m uvicorn src.main:app --host 0.0.0.0 --port $PORT`

---

### PART 2: Deploy Frontend to Vercel

#### Step 1: Create Next.js Frontend

Create file: `frontend/package.json`
```json
{
  "name": "queen-voice-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "14.2.5",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "lucide-react": "^0.400.0"
  }
}
```

Create file: `frontend/next.config.js`
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
}

module.exports = nextConfig
```

Create file: `frontend/src/app/page.js`
```jsx
'use client';

import { useState } from 'react';
import { Phone, Mic, Calendar, Users, BarChart3 } from 'lucide-react';

export default function Home() {
  const [isCalling, setIsCalling] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900">
      {/* Header */}
      <header className="p-6 border-b border-white/10">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-3xl font-bold text-white">👑 Queen Voice AI</h1>
          <nav className="space-x-6">
            <a href="#dashboard" className="text-white/80 hover:text-white">Dashboard</a>
            <a href="#calls" className="text-white/80 hover:text-white">Call Logs</a>
            <a href="#settings" className="text-white/80 hover:text-white">Settings</a>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto p-6">
        <div className="text-center py-20">
          <h2 className="text-5xl font-bold text-white mb-6">
            AI Phone Agents for Indian Businesses
          </h2>
          <p className="text-xl text-white/80 mb-8">
            Never miss a call. Book appointments 24/7. Speak Hindi & English fluently.
          </p>
          
          <button 
            onClick={() => setIsCalling(!isCalling)}
            className="bg-white text-purple-900 px-8 py-4 rounded-full text-lg font-semibold hover:bg-purple-100 transition flex items-center gap-3 mx-auto"
          >
            <Phone className="w-6 h-6" />
            {isCalling ? 'End Test Call' : 'Try Demo Call'}
          </button>

          {isCalling && (
            <div className="mt-8 p-6 bg-white/10 rounded-lg max-w-md mx-auto">
              <div className="flex items-center gap-4 text-white">
                <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                <span>Connected to +91 80654 81672</span>
              </div>
              <p className="mt-4 text-white/80">
                "Namaste! Main Queen bol rahi hoon. Kaise help kar sakti hoon?"
              </p>
            </div>
          )}
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-6 mt-20">
          <FeatureCard 
            icon={<Mic className="w-8 h-8" />}
            title="Natural Conversations"
            description="Hindi & English support with human-like voice"
          />
          <FeatureCard 
            icon={<Calendar className="w-8 h-8" />}
            title="Auto Booking"
            description="Book appointments directly into your calendar"
          />
          <FeatureCard 
            icon={<BarChart3 className="w-8 h-8" />}
            title="Analytics Dashboard"
            description="Track calls, conversions, and ROI in real-time"
          />
        </div>

        {/* Stats Section */}
        <div className="grid md:grid-cols-4 gap-6 mt-20">
          <StatCard number="500+" label="Calls Handled" />
          <StatCard number="98%" label="Answer Rate" />
          <StatCard number="<600ms" label="Response Time" />
          <StatCard number="₹0.73/min" label="Cost" />
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-white/10 mt-20 py-8">
        <div className="max-w-7xl mx-auto text-center text-white/60">
          <p>© 2025 Queen Voice AI. Built for India 🇮🇳</p>
        </div>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, description }) {
  return (
    <div className="bg-white/10 backdrop-blur-sm p-6 rounded-lg border border-white/20 hover:bg-white/20 transition">
      <div className="text-purple-300 mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-white mb-2">{title}</h3>
      <p className="text-white/70">{description}</p>
    </div>
  );
}

function StatCard({ number, label }) {
  return (
    <div className="text-center p-6 bg-white/5 rounded-lg">
      <div className="text-3xl font-bold text-purple-300 mb-2">{number}</div>
      <div className="text-white/60">{label}</div>
    </div>
  );
}
```

Create file: `frontend/src/app/layout.js`
```jsx
export const metadata = {
  title: 'Queen Voice AI - AI Phone Agents for India',
  description: '24/7 AI phone agents that speak Hindi & English. Book appointments automatically.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
```

Create file: `frontend/tailwind.config.js`
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

Create file: `frontend/.gitignore`
```
node_modules
.next
.env.local
```

#### Step 2: Push to GitHub

```bash
cd /workspace/vobiz-voice-ai
git add frontend/
git commit -m "Add Next.js frontend for Vercel deployment"
git push origin main
```

#### Step 3: Deploy to Vercel

1. Go to https://vercel.com
2. Click "Add New" → "Project"
3. Import your GitHub repo: `qween-ai-voice-calling`
4. Framework Preset: **Next.js** (auto-detected)
5. Root Directory: `frontend`
6. Environment Variables:
   ```
   NEXT_PUBLIC_API_URL=https://your-railway-app.up.railway.app
   ```
7. Click **Deploy**

🎉 Your site will be live at: `https://queen-voice-calling.vercel.app`

---

## 🔧 TROUBLESHOOTING

### Error: "No space left on device"
**Solution:** This workspace has limited storage. Develop locally or use GitHub Codespaces.

### Error: "Module not found"
**Solution:** Run `npm install` in the `frontend` folder before deploying.

### Error: "Build failed"
**Solution:** Check Vercel deployment logs. Common issues:
- Missing `next.config.js`
- Incorrect Node.js version (use 18.x)
- TypeScript errors (if using TS)

### LiveKit Agent Not Connecting
**Solution:** 
1. Ensure backend is running on Railway/Render
2. Check environment variables match exactly
3. Verify LiveKit dispatch rules are configured

---

## 💰 COST BREAKDOWN

| Service | Plan | Cost/Month |
|---------|------|------------|
| Vercel | Hobby | FREE |
| Railway | Starter | $5 (₹415) |
| LiveKit Cloud | Startup | $0.02/hr usage |
| Supabase | Free Tier | FREE |
| Vobiz | Pay-as-you-go | ₹0.67/min |
| Gemini API | Pay-as-you-go | ₹0.06/min |

**Total Fixed Cost:** ~₹500/month  
**Variable Cost:** ₹0.73/min of calls

---

## 🎯 NEXT ACTIONS

1. **Today:** Create Railway account, deploy backend
2. **Tomorrow:** Create frontend files, push to GitHub
3. **Day 3:** Deploy to Vercel
4. **Day 4:** Configure custom domain
5. **Day 5:** Demo to first dental clinic!

**Jai Hind! 🇮🇳🚀**
