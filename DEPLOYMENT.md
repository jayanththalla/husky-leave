# Deployment Guide

Step-by-step guide to deploy the Leave Management System to production.

## Prerequisites

- GitHub account with repository
- Render account (for backend)
- Vercel account (for frontend)
- MongoDB Atlas account (for database)

## Backend Deployment (Render.com)

### 1. Prepare Your Code

Make sure your backend is ready:

```bash
cd backend
# Verify all files are present
ls -la
# Should include: pyproject.toml, app/, .env.example
```

### 2. Push to GitHub

```bash
git add .
git commit -m "Initial backend setup"
git push origin main
```

### 3. Create Render Service

1. Go to [https://render.com](https://render.com)
2. Sign up/Login
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Select the repository and branch
6. Fill in the details:
   - **Name**: leave-management-api
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3` (Ensure `.python-version` or `PYTHON_VERSION=3.12.0` is used)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### 4. Set Environment Variables

In Render dashboard:
1. Go to "Environment" tab
2. Add variables:
   - **MONGODB_URI**: Your MongoDB Atlas connection string
   - **JWT_SECRET_KEY**: Generate a strong secret key
   - **JWT_ALGORITHM**: HS256
   - **JWT_EXPIRATION_HOURS**: 24
   - **ENVIRONMENT**: production

### 5. Deploy

1. Click "Create Web Service"
2. Render will automatically deploy
3. Wait for deployment to complete
4. Your backend URL will be: `https://leave-management-api.onrender.com`

## Frontend Deployment (Vercel)

### 1. Update API URL

Update `frontend/.env.production`:

```
VITE_API_BASE_URL=https://leave-management-api.onrender.com
```

### 2. Deploy on Vercel

1. Go to [https://vercel.com](https://vercel.com)
2. Import your repository
3. Configure:
   - **Framework**: Vue.js
   - **Root Directory**: frontend
4. Click "Deploy"
