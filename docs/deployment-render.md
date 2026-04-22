# Deploying ActuFlow Backend to Render

This guide covers deploying the FastAPI backend to Render.com with Neon PostgreSQL and Upstash Redis.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Pages                              │
│              (Frontend - Static React)                       │
│         https://username.github.io/actuflow                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS API calls
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Render.com                              │
│                  (FastAPI Backend)                           │
│            https://actuflow-api.onrender.com                 │
└─────────────────────────────────────────────────────────────┘
                    │                   │
                    ▼                   ▼
       ┌────────────────────┐  ┌────────────────────┐
       │    Neon.tech       │  │    Upstash         │
       │   (PostgreSQL)     │  │    (Redis)         │
       │   Free: 500MB      │  │   Free: 10k/day    │
       └────────────────────┘  └────────────────────┘
```

## Prerequisites

- GitHub account with your ActuFlow repository
- Render.com account (free)
- Neon.tech account (free)
- Upstash.com account (free)

---

## Step 1: Setup Neon PostgreSQL

### Create Database

1. Go to https://neon.tech and sign up
2. Click "Create Project"
3. Settings:
   - **Project name:** `actuflow`
   - **Database name:** `actuflow`
   - **Region:** Choose closest to your users
4. Click "Create Project"

### Get Connection String

1. In project dashboard, click "Connection Details"
2. Select "Connection string" tab
3. Copy the string (looks like):
   ```
   postgresql://username:password@ep-cool-name-123456.us-east-2.aws.neon.tech/actuflow?sslmode=require
   ```
4. Save this for later

### Enable pgvector (Optional - for AI features)

1. Go to SQL Editor in Neon dashboard
2. Run:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

---

## Step 2: Setup Upstash Redis

### Create Database

1. Go to https://upstash.com and sign up
2. Click "Create Database"
3. Settings:
   - **Name:** `actuflow-redis`
   - **Type:** Regional
   - **Region:** Same region as Neon
4. Click "Create"

### Get Connection String

1. In database dashboard, find "REST API" section
2. Click "Redis URL" to reveal
3. Copy the string (looks like):
   ```
   rediss://default:AbCdEf123456@us1-stunning-hippo-12345.upstash.io:6379
   ```
4. Save this for later

---

## Step 3: Prepare Backend for Render

### Verify requirements.txt

Ensure `backend/requirements.txt` includes:

```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
alembic>=1.12.0
asyncpg>=0.29.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
redis>=5.0.0
celery>=5.3.0
boto3>=1.33.0
pandas>=2.1.0
numpy>=1.26.0
httpx>=0.25.0
```

### Verify Procfile (Optional)

Create `backend/Procfile` if you prefer Procfile-based deployment:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## Step 4: Deploy to Render

### Create Web Service

1. Go to https://render.com and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select your `actuflow` repository

### Configure Service

**Basic Settings:**
- **Name:** `actuflow-api`
- **Region:** Same as your database
- **Branch:** `main`
- **Root Directory:** `backend`
- **Runtime:** Python 3

**Build & Deploy:**
- **Build Command:** 
  ```
  pip install -r requirements.txt && alembic upgrade head
  ```
- **Start Command:**
  ```
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

**Instance Type:**
- Select "Free" (for testing) or "Starter $7/mo" (for production)

### Add Environment Variables

Click "Environment" and add:

| Key | Value | Notes |
|-----|-------|-------|
| `DATABASE_URL` | `postgresql://...` | From Neon |
| `REDIS_URL` | `rediss://...` | From Upstash |
| `SECRET_KEY` | `<random-64-char-string>` | Generate with `openssl rand -hex 32` |
| `DEBUG` | `false` | |
| `ALLOWED_ORIGINS` | `https://yourusername.github.io` | Your GitHub Pages URL |
| `GITHUB_PAGES_URL` | `https://yourusername.github.io/actuflow` | Full frontend URL |
| `AI_ENABLED` | `false` | Disable AI for free tier |
| `PROJECT_NAME` | `ActuFlow` | |

### Deploy

1. Click "Create Web Service"
2. Wait for build (2-5 minutes)
3. Check logs for errors
4. Note your URL: `https://actuflow-api.onrender.com`

---

## Step 5: Verify Deployment

### Test Health Endpoint

```bash
curl https://actuflow-api.onrender.com/health
```

Expected response:
```json
{"status": "healthy", "service": "ActuFlow"}
```

### Test API Docs

Open in browser:
```
https://actuflow-api.onrender.com/api/v1/docs
```

You should see Swagger UI.

### Test Database Connection

```bash
curl https://actuflow-api.onrender.com/api/v1/auth/health
```

---

## Step 6: Connect Frontend

### Update GitHub Repository Variables

1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Click "Variables" tab
3. Add variable:
   - **Name:** `API_URL`
   - **Value:** `https://actuflow-api.onrender.com`

### Trigger Frontend Rebuild

1. Push any change to `main` branch, or
2. Go to Actions → Deploy to GitHub Pages → Run workflow

### Verify Connection

1. Open your GitHub Pages site
2. Open browser DevTools → Network tab
3. Try to login or make API request
4. Verify requests go to your Render URL

---

## Step 7: Deploy Celery Worker (Optional)

For background tasks (calculations, reports), deploy a worker:

### Create Background Worker

1. In Render, click "New +" → "Background Worker"
2. Same repository, same settings
3. **Root Directory:** `backend`
4. **Build Command:** `pip install -r requirements.txt`
5. **Start Command:** 
   ```
   celery -A app.celery_app worker --loglevel=info
   ```
6. Same environment variables as web service
7. Select "Free" tier

**Note:** Free tier workers have limitations. For production, use paid tier.

---

## Troubleshooting

### Build Fails

**Check logs for:**
- Missing dependencies → Add to requirements.txt
- Python version issues → Add `runtime.txt` with `python-3.12.0`

### Database Connection Fails

**Verify:**
- DATABASE_URL is correct
- Neon database is not suspended (wake it by visiting dashboard)
- SSL mode is included: `?sslmode=require`

### CORS Errors

**Verify:**
- ALLOWED_ORIGINS includes your exact GitHub Pages URL
- No trailing slash in URL
- Protocol is `https://` not `http://`

### Cold Starts (Free Tier)

Free tier services sleep after 15 minutes of inactivity.

**Solutions:**
- First request takes ~30 seconds (normal)
- Use a service like UptimeRobot to ping every 14 minutes
- Upgrade to paid tier ($7/month) for always-on

### Migration Errors

**If migrations fail:**
```bash
# Connect to Render shell
# Run migrations manually
alembic upgrade head

# Or check current state
alembic current
```

---

## Production Checklist

- [ ] SECRET_KEY is unique and secure (64+ chars)
- [ ] DEBUG is `false`
- [ ] ALLOWED_ORIGINS is restricted to your domain
- [ ] Database has SSL enabled (`sslmode=require`)
- [ ] Backups configured in Neon dashboard
- [ ] Error monitoring set up (Sentry optional)
- [ ] Custom domain configured (optional)

---

## Cost Summary (Free Tier)

| Service | Free Tier Limits | Monthly Cost |
|---------|-----------------|---------------|
| Render Web | 750 hrs, sleeps after 15min | $0 |
| Render Worker | 750 hrs, sleeps | $0 |
| Neon PostgreSQL | 500MB, suspends after 5min | $0 |
| Upstash Redis | 10k commands/day | $0 |
| **Total** | | **$0** |

### Paid Upgrade Path

| Service | Starter Tier | Monthly Cost |
|---------|--------------|---------------|
| Render Web | Always on, 512MB RAM | $7 |
| Render Worker | Always on | $7 |
| Neon PostgreSQL | 3GB, never suspends | $19 |
| Upstash Redis | 10M commands/day | $10 |
| **Total** | | **$43** |
