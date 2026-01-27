# Railway Deployment Guide

This repository contains both backend and frontend services that should be deployed as **two separate Railway services**.

## Architecture

- **Backend**: FastAPI application (`app/main.py`)
- **Frontend**: React + Vite application (`quantdashboard/`)

---

## Backend Service Configuration

### Railway Settings

1. **Service Name**: `quant-backend` (or your preferred name)
2. **Root Directory**: `/` (repository root)
3. **Build Command**: (leave empty - Railway auto-detects Python)
4. **Start Command**: (leave empty - uses Procfile)

### Environment Variables

Add these in Railway dashboard → Variables:

```
DATABASE_URL=postgresql://user:pass@host:port/dbname
TRADING_CORS_ORIGINS=https://your-frontend-domain.railway.app
PORT=8000
```

**Note**: Railway automatically provides `DATABASE_URL` if you add a PostgreSQL service. `PORT` is set automatically by Railway.

### Procfile

The `Procfile` in the root directory contains:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Railway will automatically use this.

---

## Frontend Service Configuration

### Railway Settings

1. **Service Name**: `quant-frontend` (or your preferred name)
2. **Root Directory**: `quantdashboard`
3. **Build Command**: `npm run build`
4. **Start Command**: `npm run start`

### Environment Variables

Add these in Railway dashboard → Variables:

```
VITE_API_BASE_URL=https://your-backend-domain.railway.app
PORT=3000
```

**Important**: Replace `your-backend-domain.railway.app` with your actual backend Railway URL.

### Package.json Scripts

The frontend uses:
- `npm run build` - Builds production assets to `dist/`
- `npm run start` - Serves the built files (uses `vite preview`)

---

## Step-by-Step Deployment

### 1. Deploy Backend

1. In Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"** (or use Railway CLI)
3. Choose this repository
4. Railway will detect Python → click **"Add Service"**
5. Set **Root Directory** to `/` (default)
6. Add environment variables:
   - `TRADING_CORS_ORIGINS=https://your-frontend-url.railway.app` (update after frontend deploys)
7. Add PostgreSQL database (optional, but recommended):
   - Click **"New"** → **"Database"** → **"Add PostgreSQL"**
   - Railway auto-sets `DATABASE_URL`
8. Deploy → Railway will use `Procfile` automatically

### 2. Deploy Frontend

1. In the same Railway project, click **"New Service"**
2. Select **"Deploy from GitHub repo"** → same repository
3. Railway will detect Node.js → click **"Add Service"**
4. Set **Root Directory** to `quantdashboard`
5. Set **Build Command** to: `npm run build`
6. Set **Start Command** to: `npm run start`
7. Add environment variable:
   - `VITE_API_BASE_URL=https://your-backend-url.railway.app`
   - (Get backend URL from Railway dashboard → backend service → Settings → Domains)
8. Deploy

### 3. Update CORS

After frontend deploys:
1. Copy frontend Railway URL
2. Go to backend service → Variables
3. Update `TRADING_CORS_ORIGINS` to: `https://your-frontend-url.railway.app`
4. Redeploy backend (or it will auto-redeploy)

---

## Local Testing (Production-like)

### Test Backend Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TRADING_CORS_ORIGINS="http://localhost:3000"
export PORT=8000

# Run with Procfile command
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Test Frontend Locally (Production Build)

```bash
cd quantdashboard

# Install dependencies
npm install

# Build production assets
npm run build

# Set API URL
export VITE_API_BASE_URL="http://localhost:8000"
export PORT=3000

# Serve production build
npm run start
```

Then visit `http://localhost:3000` - it should connect to backend at `http://localhost:8000`.

---

## Verification Checklist

- [ ] Backend service is running and accessible
- [ ] Frontend service is running and accessible
- [ ] Frontend can fetch from `/status` endpoint (check browser console)
- [ ] CORS headers are correct (backend allows frontend origin)
- [ ] Environment variables are set correctly
- [ ] Both services have custom domains (optional but recommended)

---

## Troubleshooting

### Backend Issues

- **Port binding**: Railway sets `PORT` automatically - don't hardcode it
- **CORS errors**: Ensure `TRADING_CORS_ORIGINS` includes your frontend URL (with `https://`)
- **Database**: If using PostgreSQL, ensure `DATABASE_URL` is set correctly

### Frontend Issues

- **API calls failing**: Check `VITE_API_BASE_URL` matches backend URL exactly
- **Build fails**: Ensure Node.js version is compatible (Railway auto-detects)
- **404 on refresh**: Vite preview handles SPA routing, but ensure Railway serves `index.html` for all routes

### Common Fixes

1. **Frontend shows mock data**: Backend URL incorrect or CORS blocking
2. **502 Bad Gateway**: Service crashed - check Railway logs
3. **Build timeout**: Increase build timeout in Railway settings

---

## File Structure Reference

```
/
├── Procfile                    # Backend start command
├── requirements.txt            # Backend Python dependencies
├── app/
│   ├── main.py                # Backend entry point
│   └── ...
├── quantdashboard/
│   ├── package.json           # Frontend dependencies & scripts
│   ├── vite.config.ts         # Vite configuration
│   └── ...
└── RAILWAY.md                 # This file
```

---

## Quick Reference

### Backend
- **Entry**: `app/main.py`
- **Start**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Deps**: `requirements.txt`

### Frontend
- **Root**: `quantdashboard/`
- **Build**: `npm run build`
- **Start**: `npm run start`
- **Deps**: `package.json`

---

## Support

For Railway-specific issues, see [Railway Docs](https://docs.railway.app).

