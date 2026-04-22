# ActuFlow Quick Start Guide

## Step 1: Prepare Docker

### Windows Users - IMPORTANT
1. Open Docker Desktop
2. Go to Settings → Resources
3. Set Memory to **8GB minimum** (12GB recommended)
4. Set CPUs to **4 minimum**
5. Click "Apply & Restart"
6. Wait for Docker to fully restart

### Clean Previous Attempts
```powershell
# Run these commands in PowerShell
docker-compose down -v
docker system prune -a --volumes -f
docker builder prune -a -f
```

## Step 2: Setup Environment

```powershell
# Copy environment file
copy .env.example .env
```

## Step 3: Start Services (Minimal)

```powershell
# Start only essential services first
docker-compose up -d postgres redis

# Wait 30 seconds for them to be ready
Start-Sleep 30

# Check they're running
docker-compose ps
```

## Step 4: Build and Start Backend

```powershell
# Build backend (should take 2-5 minutes)
docker-compose build backend

# Start backend
docker-compose up -d backend

# Check logs
docker-compose logs -f backend
```

## Step 5: Build and Start Frontend

```powershell
# Build frontend (should take 1-3 minutes)
docker-compose build frontend

# Start frontend
docker-compose up -d frontend

# Check logs
docker-compose logs -f frontend
```

## Step 6: Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs
- Login: admin@actuflow.com / admin123

## Troubleshooting

### Docker Crashes / Bus Error
1. Close Docker Desktop completely
2. Open Task Manager → End all Docker processes
3. Restart Docker Desktop
4. Increase memory allocation

### Build Takes Forever
```powershell
# Cancel with Ctrl+C, then:
docker-compose down
docker builder prune -f
# Try building again
```

### Port Already in Use
```powershell
# Find what's using port 5432 (example)
netstat -ano | findstr :5432

# Kill process by PID
taskkill /PID <PID> /F
```

### Still Not Working?
Try a single service at a time:
```powershell
docker-compose up postgres -d
docker-compose up redis -d
docker-compose up backend -d
docker-compose up frontend -d
```
