# Deploy ActuFlow Frontend to Vercel

## Prerequisites

1. GitHub account with your code pushed
2. Vercel account (https://vercel.com - sign up with GitHub)
3. Backend API deployed (on Railway or another service)

## Step-by-Step Deployment

### 1. Connect GitHub to Vercel

1. Go to https://vercel.com
2. Click "New Project"
3. Import your GitHub repository
4. Select your `actuflow` repository

### 2. Configure Project Settings

1. **Project Name**: `actuflow` (or your preferred name)
2. **Framework Preset**: Vite
3. **Root Directory**: Leave as default (./frontend will be auto-detected if needed)
4. Click "Configure" if you need to set it explicitly:
   - Set **Root Directory** to: `frontend`

### 3. Set Environment Variables

Before deploying, add environment variables in Vercel:

1. Click "Environment Variables"
2. Add the following variables:

```
VITE_API_URL: https://your-backend-api.railway.app
VITE_AI_ENABLED: true
```

Replace `https://your-backend-api.railway.app` with your actual backend URL from Railway.

### 4. Deploy

1. Click "Deploy"
2. Vercel will automatically build and deploy your frontend
3. You'll get a `.vercel.app` URL for your live application

### 5. Connect Backend API

After deployment, your frontend will be running on Vercel. To connect it to your backend:

1. If your backend is on Railway:
   - Ensure `VITE_API_URL` points to your Railway backend URL
   - CORS should be configured on your backend to allow requests from your Vercel domain

2. Update your backend CORS settings in `backend/app/config.py`:
   ```python
   ALLOWED_ORIGINS = [
       "http://localhost:3000",
       "http://localhost:8000",
       "https://your-vercel-domain.vercel.app",  # Your Vercel URL
   ]
   ```

### 6. Update Backend for Vercel Domain

After getting your Vercel URL:

1. Update `backend/app/config.py` with your Vercel domain
2. Redeploy backend to Railway
3. Test the frontend → backend communication

## Continuous Deployment

Vercel will automatically redeploy whenever you push to your GitHub repository (main branch by default).

### Using a Different Branch

1. In Vercel Dashboard → Settings → Git
2. Change the "Production Branch" to your desired branch

## Rollback

To rollback to a previous deployment:

1. In Vercel Dashboard → Deployments
2. Find the previous deployment
3. Click the three dots → "Promote to Production"

## Troubleshooting

### CORS Errors

If you see CORS errors in the browser console:
- Check that your backend's `ALLOWED_ORIGINS` includes your Vercel URL
- Ensure your backend is properly deployed and accessible

### API Calls Failing

- Verify `VITE_API_URL` environment variable is set correctly
- Check Network tab in browser dev tools to see actual API URLs being called
- Ensure backend is running and accessible from your Vercel domain

### Build Failures

Check the Vercel build logs:
1. Go to Vercel Dashboard → Select your project
2. Click "Deployments"
3. Find the failed deployment
4. Click "View Logs" to see what went wrong

## Optional: Custom Domain

To use a custom domain:

1. In Vercel Dashboard → Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

## Multiple Environments

To deploy different environments (staging, production):

1. Create separate GitHub branches (e.g., `staging`, `main`)
2. Create separate Vercel projects for each
3. Connect each project to different branches
