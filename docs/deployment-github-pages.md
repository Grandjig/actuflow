# Deploying ActuFlow to GitHub Pages

## Overview

GitHub Pages can host the **frontend only**. The backend (FastAPI, PostgreSQL, Redis, Celery) must be hosted elsewhere.

## Architecture for GitHub Pages Deployment

```
┌─────────────────────────────────────────────────────────────┐
│ GitHub Pages │
│ (Static Frontend) │
│ https://username.github.io/actuflow │
└─────────────────────────────────────────────────────────────┘
 │
 │ HTTPS API calls
 ▼
┌─────────────────────────────────────────────────────────────┐
│ Backend Host (Render / Fly.io / Railway) │
│ https://actuflow-api.onrender.com │
├─────────────────────────────────────────────────────────────┤
│ FastAPI Backend │
│ Celery Workers │
└─────────────────────────────────────────────────────────────┘
 │
 ▼
┌─────────────────────────────────────────────────────────────┐
│ Managed Services │
├─────────────────────┬───────────────────────────────────────┤
│ Neon / Supabase │ Upstash │
│ (PostgreSQL) │ (Redis) │
│ Free: 500MB-1GB │ Free: 10k commands/day │
└─────────────────────┴───────────────────────────────────────┘
```

## Step 1: Setup GitHub Pages

### Enable GitHub Pages

1. Go to your repo → Settings → Pages
2. Source: "GitHub Actions"
3. The workflow will deploy automatically on push to `main`

### Configure Repository Variables

1. Go to Settings → Secrets and variables → Actions → Variables
2. Add variable: `API_URL` = `https://your-backend-url.onrender.com`

## Step 2: Deploy Backend to Render (Free Tier)

### Create Render Account

1. Sign up at https://render.com
2. Connect your GitHub repository

### Create Web Service

1. New → Web Service
2. Connect repository
3. Configure:
 - Name: `actuflow-api`
 - Root Directory: `backend`
 - Runtime: Python 3
 - Build Command: `pip install -r requirements.txt`
 - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Environment Variables (Render)

```
DATABASE_URL=postgresql://... (from Neon)
REDIS_URL=redis://... (from Upstash)
SECRET_KEY=generate-a-secure-key
ALLOWED_ORIGINS=https://username.github.io
```

## Step 3: Setup Database (Neon - Free)

1. Sign up at https://neon.tech
2. Create project "actuflow"
3. Copy connection string
4. Add to Render environment variables

## Step 4: Setup Redis (Upstash - Free)

1. Sign up at https://upstash.com
2. Create Redis database
3. Copy connection string
4. Add to Render environment variables

## Step 5: Configure CORS

Update backend to allow GitHub Pages origin:

```python
# backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
 CORSMiddleware,
 allow_origins=[
 "https://username.github.io",
 "http://localhost:3000", # Local dev
 ],
 allow_credentials=True,
 allow_methods=["*"],
 allow_headers=["*"],
)
```

## Free Tier Limitations

| Service | Limitation | Impact |
|---------|------------|--------|
| GitHub Pages | Static files only | Frontend only |
| Render Free | Sleeps after 15min inactivity | Cold start ~30s |
| Neon Free | 500MB storage | ~50k policies |
| Upstash Free | 10k commands/day | Light usage only |

## Alternative Backend Hosts

| Provider | Free Tier | Notes |
|----------|-----------|-------|
| Render | 750 hrs/mo | Sleeps on inactivity |
| Fly.io | 3 shared VMs | Generous free tier |
| Railway | $5 credit/mo | Simple setup |
| Koyeb | 2 nano instances | Good free tier |

## Local Development

For local development, frontend still proxies to local backend:

```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

## Deploying Updates

### Frontend (Automatic)
Push to `main` branch → GitHub Actions builds and deploys

### Backend (Automatic with Render)
Push to `main` branch → Render auto-deploys

## Troubleshooting

### CORS Errors
- Verify `ALLOWED_ORIGINS` includes your GitHub Pages URL
- Check browser console for specific CORS error

### 404 on Page Refresh
- The `404.html` redirect handles this for GitHub Pages
- Make sure it's in `frontend/public/`

### API Connection Failed
- Verify `VITE_API_URL` is set correctly
- Check if backend is awake (free tier sleeps)
- Test API directly: `curl https://your-api.onrender.com/health`
