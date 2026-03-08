# Leave Management System - Backend API

Python FastAPI backend for the Leave Management System with MongoDB integration.

## Setup Instructions

### 1. Install Python and Dependencies

```bash
cd backend
uv init --bare .
uv add fastapi uvicorn python-dotenv pymongo pydantic pydantic-settings bcrypt python-jose pyjwt passlib python-multipart
```

### 2. Configure Environment Variables

Create a `.env` file in the backend directory:

```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/leave_management?retryWrites=true&w=majority
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
ENVIRONMENT=development
```

Get MongoDB URI from MongoDB Atlas (free tier available).

### 3. Run the Server

```bash
uv run python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- Interactive API docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /api/users/register` - Register new user
- `POST /api/users/login` - Login user
- `GET /api/users/me` - Get current user profile

### Leave Requests
- `POST /api/leaves/request` - Create leave request (Employee)
- `GET /api/leaves/my-requests` - Get own leave requests (Employee)
- `GET /api/leaves/all` - Get all requests (Employer)
- `PATCH /api/leaves/{request_id}` - Update request status (Employer)

## Deployment

Deploy to Render.com:
1. Push code to GitHub
2. Connect repository to Render
3. Set environment variables in Render dashboard
4. Deploy as Web Service with `uvicorn app.main:app --host 0.0.0.0 --port 8000`
