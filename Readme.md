# Csyrus Workflow Approval Management System

## Project Overview

The Csyrus Workflow Approval Management System is a full-stack web application built for the Csyrus Technologies Engineering Internship Assessment.

The system allows Requesters to create and manage approval requests while Reviewers can review, approve, or reject those requests with comments.

Authentication is implemented exclusively using Google OAuth 2.0, following the assessment requirements:

Login with Google → Google Consent Screen → Successful Authentication → JWT Session Created → Protected Application Access

---

# Tech Stack

## Backend

* Python 3.x
* FastAPI
* SQLAlchemy ORM
* PostgreSQL
* Alembic
* PyJWT
* Pytest

## Frontend

* React.js
* Vite
* React Router
* Axios
* React Testing Library
* Vitest

## Authentication

* Google OAuth 2.0
* JWT Authentication

---

# Project Structure

## Backend

```text
backend/
├── app/
│   ├── api/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── core/
│   └── database/
├── tests/
└── main.py
```

## Frontend

```text
frontend/
└── src/
    ├── api/
    ├── components/
    ├── pages/
    ├── routes/
    ├── hooks/
    ├── services/
    ├── context/
    ├── utils/
    └── tests/
```

---

# Features

## Requester

* Login using Google OAuth
* Create approval requests
* View own requests
* Update pending requests
* Delete pending requests
* Track request status

## Reviewer

* View assigned requests
* Approve requests
* Reject requests
* Add review comments
* View request details

---

# Database Setup

Create PostgreSQL database:

```sql
CREATE DATABASE csyrus_db;
```

---

# Environment Variables

## Backend (.env)

```env
PROJECT_NAME=Csyrus Workflow Approval API
VERSION=1.0.0
API_V1_STR=/api/v1

DATABASE_URL=postgresql://postgres:rishabh@localhost:5432/csyrus_db

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

FRONTEND_URL=http://localhost:5173
```

## Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

---

# Google OAuth Setup

## Create OAuth Credentials

1. Open Google Cloud Console.
2. Create a new project.
3. Configure OAuth Consent Screen.
4. Select External User Type.
5. Add the following scopes:

```text
openid
email
profile
```

6. Add yourself as a Test User.

---

## Create OAuth Client

Application Type:

```text
Web Application
```

Authorized JavaScript Origins:

```text
http://localhost:5173
```

Authorized Redirect URI:

```text
http://localhost:8000/api/v1/auth/google/callback
```

Copy:

* GOOGLE_CLIENT_ID
* GOOGLE_CLIENT_SECRET

And place them inside backend/.env.

---

# Backend Setup

Navigate to backend folder:

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
alembic upgrade head
```

Start backend server:

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

# Frontend Setup

Navigate to frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run application:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

# Running Tests

## Backend Tests

```bash
cd backend

pytest -v
```

Expected Output:

```text
========================
PASSED
========================
```

---

## Frontend Tests

```bash
cd frontend

npm test
```

or

```bash
npm run test
```

Expected Output:

```text
All tests passed
```

---

# API Documentation

## Authentication

| Method | Endpoint                     |
| ------ | ---------------------------- |
| GET    | /api/v1/auth/google/login    |
| GET    | /api/v1/auth/google/callback |
| GET    | /api/v1/auth/me              |

---

## Requester APIs

| Method | Endpoint              |
| ------ | --------------------- |
| POST   | /api/v1/requests      |
| GET    | /api/v1/requests      |
| GET    | /api/v1/requests/{id} |
| PUT    | /api/v1/requests/{id} |
| DELETE | /api/v1/requests/{id} |

---

## Reviewer APIs

| Method | Endpoint                               |
| ------ | -------------------------------------- |
| GET    | /api/v1/reviewer/requests              |
| POST   | /api/v1/reviewer/requests/{id}/approve |
| POST   | /api/v1/reviewer/requests/{id}/reject  |

---

# Authentication Flow

```text
User
 ↓
Login With Google
 ↓
Google Consent Screen
 ↓
Google Callback
 ↓
Backend Validates User
 ↓
JWT Generated
 ↓
JWT Stored
 ↓
Protected Routes Accessible
```

---

# Running the Complete Application

Terminal 1:

```bash
cd backend
uvicorn app.main:app --reload
```

Terminal 2:

```bash
cd frontend
npm run dev
```

Open:

```text
http://localhost:5173
```

Login with Google and start using the application.

---

# Documentation Files

The repository includes:

* README.md
* ENGINEERING_DECISIONS.md
* COLLABORATION.md
* Architecture Diagram

---

# Scalability Considerations

* Layered architecture (API → Service → Repository → Database)
* SQLAlchemy ORM abstraction
* Role-based access control
* JWT authentication
* Modular React component structure
* Reusable API layer
* Testable business logic

---

# Assessment Deliverables

* Backend Repository
* Frontend Repository
* Architecture Diagram
* Demo Video
* Unit Tests
* Pull Request
* Documentation

All assessment requirements have been implemented using the mandated technology stack and project structure.
