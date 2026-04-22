# Deploy ActuFlow to Railway

## Prerequisites

1. GitHub account with your code pushed
2. Railway account (https://railway.app - sign up with GitHub)

## Step-by-Step Deployment

### 1. Create Railway Project

1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select your `actuflow` repository
4. Railway will detect the monorepo structure

### 2. Add PostgreSQL Database

1. In your Railway project, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway automatically creates and connects it
4. Note: Railway provides `DATABASE_URL` automatically

### 3. Add Redis

1. Click "+ New" again
2. Select "Database" → "Redis"
3. Railway provides `REDIS_URL` automatically

### 4. Deploy Backend

1. Click "+ New" → "GitHub Repo"
2. Select your repo again
3. Click on the service, go to "Settings"
4. Set **Root Directory**: `backend`
5. Go to "Variables" tab and add:

```
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=${{Redis.REDIS_URL}}
JWT_SECRET=your-super-secret-key-change-this
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
DEBUG=false
AI_ENABLED=false
```

6. Deploy will start automatically

### 5. Deploy Frontend

1. Click "+ New" → "GitHub Repo"
2. Select your repo again
3. Go to "Settings"
4. Set **Root Directory**: `frontend`
5. Go to "Variables" and add:

```
VITE_API_URL=https://[your-backend-service].up.railway.app
```

(Get the backend URL from the backend service's "Settings" → "Domains")

### 6. Generate Domain URLs

1. Click on Backend service → Settings → Generate Domain
2. Click on Frontend service → Settings → Generate Domain
3. Update Frontend's `VITE_API_URL` with the actual backend URL
4. Redeploy frontend

### 7. Initialize Database

Once backend is deployed:

1. Go to Backend service
2. Click "Shell" tab (or use Railway CLI)
3. Run:

```bash
python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"
```

4. Seed the database:

```bash
python -c "
import asyncio
from app.database import async_session_factory
from app.models.user import User
from app.models.role import Role
from app.services.auth_service import get_password_hash
from sqlalchemy import select

async def seed():
    async with async_session_factory() as db:
        result = await db.execute(select(User).limit(1))
        if result.scalar_one_or_none():
            print('Already seeded')
            return
        role = Role(name='admin', description='Admin')
        db.add(role)
        await db.flush()
        user = User(
            email='admin@actuflow.com',
            hashed_password=get_password_hash('admin123'),
            full_name='Administrator',
            is_active=True,
            is_superuser=True,
            role_id=role.id,
        )
        db.add(user)
        await db.commit()
        print('Seeded: admin@actuflow.com / admin123')

asyncio.run(seed())
"
```

## Your Live URLs

After deployment:

- **Frontend**: `https://actuflow-frontend-production.up.railway.app` (or similar)
- **Backend API**: `https://actuflow-backend-production.up.railway.app/docs`

## Demo Credentials

- Email: `admin@actuflow.com`
- Password: `admin123`

## Troubleshooting

### Backend won't start

Check logs in Railway dashboard. Common issues:
- Missing environment variables
- Database not ready yet (wait a minute)

### Frontend shows blank page

- Check browser console (F12)
- Verify `VITE_API_URL` is set correctly
- Make sure backend CORS allows frontend domain

### Database connection errors

- Verify `DATABASE_URL` variable is linked to Postgres
- Railway should auto-inject this if you use `${{Postgres.DATABASE_URL}}`

## Cost

Railway pricing:
- Free tier: $5 credit/month (enough for demo)
- Hobby: $5/month (more resources)
- Pro: $20/month (production ready)

For a demo, free tier is fine!
