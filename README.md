# Leave Management System

A simple and functional web application for employees to apply for leave and for employers to manage those requests. Built with **Vue.js 3** and **FastAPI**.

## Core Features

- **Authentication**: Role-based signup and login (Employee/Employer).
- **Employee Portal**:
  - Submit leave requests with type, dates, and reason.
  - Real-time status tracking (Pending, Approved, Rejected).
  - View decision remarks from management.
- **Employer Portal**:
  - Global view of all employee leave applications.
  - Approve or Reject requests with specific remarks.
  - Status-based filtering for efficient management.

## Tech Stack

- **Frontend**: Vue.js 3, Vite, Pinia, Tailwind CSS.
- **Backend**: FastAPI (Python), PyMongo, Pydantic.
- **Database**: MongoDB Atlas.
- **Auth**: JWT (JSON Web Tokens).

## Quick Start

### 1. Prerequisites
- Python 3.9+
- Node.js 18+
- MongoDB Atlas account

### 2. Backend Setup
```bash
cd backend
cp .env.example .env
# Update MONGODB_URI and JWT_SECRET_KEY in .env

# Install and Run
uv run python -m uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
cp .env.example .env.local
# Verify VITE_API_BASE_URL in .env.local

# Install and Run
npm install
npm run dev
```

The application will be available at `http://localhost:5173`.

## Environment Variables

### Backend (.env)
- `MONGODB_URI`: MongoDB connection string.
- `JWT_SECRET_KEY`: Secret for signing tokens.
- `JWT_ALGORITHM`: Usually `HS256`.

### Frontend (.env.local)
- `VITE_API_BASE_URL`: URL of the running backend API.

## Project Structure
- `backend/`: FastAPI application, models, and routes.
- `frontend/`: Vue.js components, stores, and styles.
- `README.md`: This file.
