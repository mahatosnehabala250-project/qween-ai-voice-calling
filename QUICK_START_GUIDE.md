# 🚀 QUICK START GUIDE - Vobiz Voice AI Platform

## ⚡ Get Running in 15 Minutes!

### Step 1: Install Dependencies (3 min)

```bash
cd /workspace/vobiz-voice-ai

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Setup Environment Variables (2 min)

```bash
# Copy example file
cp .env.example .env

# Edit with your API keys (use nano, vim, or VS Code)
nano .env
```

**Required API Keys:**
- `VOBIZ_API_KEY` - From https://vobiz.ai/
- `GOOGLE_API_KEY` - From Google Cloud Console (enable Gemini API)
- `SUPABASE_URL` & `SUPABASE_KEYS` - From https://supabase.com/ (Mumbai region)

### Step 3: Start Infrastructure (5 min)

```bash
cd docker

# Start PostgreSQL, Redis, and n8n
docker-compose up -d supabase-db redis n8n

# Check if running
docker-compose ps
```

Expected output:
```
NAME                    STATUS
vobiz-supabase-db       Up
vobiz-redis             Up
vobiz-n8n               Up
```

### Step 4: Initialize Database (2 min)

```bash
# Get container name
docker ps | grep postgres

# Initialize schema
docker exec -i <container_name> psql -U postgres -d vobiz_voice_ai < init.sql
```

### Step 5: Run the Application (1 min)

```bash
cd ..

# Start FastAPI server
python -m uvicorn src.main:app --reload

# Or use: python src/main.py
```

Visit: http://localhost:8000/docs

You should see FastAPI Swagger UI! 🎉

---

## ✅ Verify Everything Works

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

Expected: `{"status": "healthy"}`

### Test 2: Check API Docs
Open browser: http://localhost:8000/docs

You should see 3 endpoints:
- `/api/v1/calls/*`
- `/api/v1/webhooks/*`
- `/api/v1/analytics/*`

### Test 3: Check n8n
Open browser: http://localhost:5678

Import workflow:
1. Go to Workflows → Import
2. Select `workflows/post-call-processing.json`
3. Click "Activate"

### Test 4: Check Database
```bash
docker exec -it <postgres_container> psql -U postgres -d vobiz_voice_ai

# Run query:
SELECT * FROM businesses;
```

---

## 🐛 Troubleshooting

### Error: "Module not found"
```bash
# Make sure you're in virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "Connection refused" on port 5432
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart if needed
docker-compose restart supabase-db
```

### Error: "API key missing"
```bash
# Check .env file exists and has values
cat .env | grep API_KEY

# Should show your actual keys, not placeholders
```

### Error: "Port already in use"
```bash
# Find what's using the port
lsof -i :8000

# Kill the process or change port in .env
SERVER_PORT=8001
```

---

## 📞 Make Your First Test Call

Once everything is running:

```bash
curl -X POST http://localhost:8000/api/v1/calls/start \
  -H "Content-Type: application/json" \
  -d '{
    "business_id": "your-business-id",
    "caller_phone": "+919876543210",
    "call_direction": "inbound"
  }'
```

---

## 🎯 Next Steps

1. **Read START_HERE.md** - Complete 7-day MVP plan
2. **Get Vobiz credentials** - Contact sales if needed
3. **Test Gemini Live** - Use Google Cloud console
4. **Customize agent prompt** - Edit `src/integrations/gemini_live.py`
5. **Find first pilot customer** - Call local dental clinics!

---

## 📚 File Reference

| File | Purpose |
|------|---------|
| `src/main.py` | FastAPI application entry point |
| `src/config.py` | Environment configuration |
| `src/routes/calls.py` | Call management endpoints |
| `src/integrations/gemini_live.py` | Gemini 2.5 Live integration |
| `src/integrations/vobiz.py` | Vobiz telephony client |
| `src/integrations/n8n.py` | n8n automation client |
| `docker/docker-compose.yml` | All services (DB, Redis, n8n) |
| `docker/init.sql` | Database schema |
| `workflows/post-call-processing.json` | n8n workflow |

---

**Need Help?** Check IMPLEMENTATION_PLAN.md for detailed roadmap.

**Jai Hind! 🇮🇳**
