# Railway Deployment - Step by Step Guide

## Prerequisites
✅ Code is pushed to: https://github.com/MAK2314/QUANTSYS.git

---

## Step 1: Create Railway Project

1. Go to https://railway.app
2. Sign in with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Authorize Railway to access your GitHub if prompted
6. Select repository: **MAK2314/QUANTSYS**
7. Click **"Deploy Now"**

---

## Step 2: Deploy Backend Service

Railway will auto-detect Python and create a service. Configure it:

### Settings:
- **Service Name**: `quant-backend` (or leave default)
- **Root Directory**: `/` (leave empty - uses root)
- **Build Command**: (leave empty - auto-detected)
- **Start Command**: (leave empty - uses `Procfile`)

### Environment Variables:
Click **"Variables"** tab and add:

```
TRADING_CORS_ORIGINS=https://your-frontend-url.railway.app
```

**Note**: You'll update this after frontend deploys. For now, you can leave it empty or use a placeholder.

### Optional: Add PostgreSQL Database
1. In the same project, click **"New"** → **"Database"** → **"Add PostgreSQL"**
2. Railway auto-sets `DATABASE_URL` environment variable

### Deploy:
- Railway will automatically detect `Procfile` and start the backend
- Wait for deployment to complete (green checkmark)
- Copy the **public domain** URL (e.g., `quant-backend-production.up.railway.app`)

---

## Step 3: Deploy Frontend Service

1. In the same Railway project, click **"New Service"**
2. Select **"Deploy from GitHub repo"**
3. Select the same repository: **MAK2314/QUANTSYS**
4. Click **"Add Service"**

### Settings:
- **Service Name**: `quant-frontend` (or leave default)
- **Root Directory**: `quantdashboard` ⚠️ **IMPORTANT**
- **Build Command**: `npm run build`
- **Start Command**: `npm run start`

### Environment Variables:
Click **"Variables"** tab and add:

```
VITE_API_BASE_URL=https://your-backend-url.railway.app
```

**Replace** `your-backend-url.railway.app` with the backend URL you copied in Step 2.

### Deploy:
- Railway will build and deploy the frontend
- Wait for deployment to complete
- Copy the **public domain** URL (e.g., `quant-frontend-production.up.railway.app`)

---

## Step 4: Update Backend CORS

1. Go back to **Backend Service** → **Variables**
2. Update `TRADING_CORS_ORIGINS` to your frontend URL:
   ```
   TRADING_CORS_ORIGINS=https://quant-frontend-production.up.railway.app
   ```
3. Railway will auto-redeploy the backend

---

## Step 5: Verify Deployment

1. **Backend Health Check**: Visit `https://your-backend-url.railway.app/`
   - Should return: `{"status":"ok","service":"Quant Backend"}`

2. **Backend Status Endpoint**: Visit `https://your-backend-url.railway.app/status`
   - Should return JSON with wallets and metrics

3. **Frontend**: Visit `https://your-frontend-url.railway.app`
   - Dashboard should load and connect to backend
   - Check browser console for any CORS errors

---

## Troubleshooting

### Backend Issues:
- **502 Bad Gateway**: Check logs → Service might be crashing
- **CORS Errors**: Ensure `TRADING_CORS_ORIGINS` includes frontend URL (with `https://`)
- **Port Issues**: Railway sets `PORT` automatically - don't override it

### Frontend Issues:
- **API Calls Failing**: Verify `VITE_API_BASE_URL` matches backend URL exactly
- **Build Fails**: Check logs → Ensure Node.js version is compatible
- **Shows Mock Data**: Backend URL incorrect or CORS blocking requests

### Common Fixes:
1. **Check Service Logs**: Click service → "Deployments" → Click latest deployment → "View Logs"
2. **Redeploy**: Click "Redeploy" button if needed
3. **Environment Variables**: Double-check all env vars are set correctly

---

## Quick Reference

### Backend Service:
- **Root**: `/` (repository root)
- **Start**: Uses `Procfile` → `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Env Vars**: `TRADING_CORS_ORIGINS`, `DATABASE_URL` (auto-set if PostgreSQL added)

### Frontend Service:
- **Root**: `quantdashboard`
- **Build**: `npm run build`
- **Start**: `npm run start`
- **Env Vars**: `VITE_API_BASE_URL`

---

## Next Steps After Deployment

1. ✅ Both services deployed
2. ✅ CORS configured
3. ✅ Frontend connected to backend
4. 🎉 Your trading dashboard is live!

You can now:
- Access the dashboard at your frontend URL
- Make API calls to backend endpoints
- Monitor logs in Railway dashboard
- Set up custom domains (optional)

---

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

