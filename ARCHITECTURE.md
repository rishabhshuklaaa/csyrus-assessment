# System Architecture & Authentication Flow

This document describes the overall architecture of the Workflow Approval Management System and the authentication flow implemented using Google OAuth 2.0 and JWT-based sessions.

---

# 🏗️ System Architecture Diagram

```mermaid
graph TD

    User[End User]

    subgraph Frontend
        React[React + Vite]
        Router[React Router]
        Axios[Axios API Client]
    end

    subgraph Backend
        API[FastAPI API Layer]
        Service[Service Layer]
        Repo[Repository Layer]
        Auth[JWT Authentication]
    end

    subgraph Database
        DB[(PostgreSQL)]
    end

    subgraph External Service
        Google[Google OAuth 2.0]
    end

    User --> React

    React --> Router
    React --> Axios

    Axios --> API

    API --> Auth
    API --> Service
    Service --> Repo
    Repo --> DB

    React --> Google
    Google --> API
```

---

# 🔐 Authentication Flow

```mermaid
sequenceDiagram

    actor User
    participant Frontend as React Frontend
    participant Google as Google OAuth
    participant Backend as FastAPI Backend
    participant Database as PostgreSQL

    User->>Frontend: Click "Login with Google"
    Frontend->>Google: Redirect to OAuth Consent Screen

    Google->>User: Authenticate & Grant Permission
    User->>Google: Approve Access

    Google->>Backend: OAuth Callback with Authorization Code

    Backend->>Google: Exchange Code for User Profile
    Google-->>Backend: User Information

    Backend->>Database: Create / Update User Record

    Backend->>Backend: Generate JWT Session

    Backend-->>Frontend: Return JWT

    Frontend->>Backend: Access Protected Routes using JWT

    Backend-->>Frontend: Authorized Response
```

---

# 📋 Architecture Overview

## Frontend

The frontend is built using:

* React.js
* Vite
* React Router
* Axios

Responsibilities:

* User authentication initiation
* Dashboard rendering
* Request creation and management
* Reviewer workflows
* Protected route handling

---

## Backend

The backend is built using:

* FastAPI
* SQLAlchemy ORM
* PostgreSQL

The backend follows a layered architecture:

```text
API Layer
    ↓
Service Layer
    ↓
Repository Layer
    ↓
Database Layer
```

Responsibilities:

* Google OAuth integration
* JWT generation and validation
* Request lifecycle management
* Reviewer approval/rejection workflow
* Business rule enforcement
* Database operations

---

## Database

PostgreSQL stores:

### Users

* id
* name
* email
* google_id
* role
* created_at

### Approval Requests

* id
* title
* description
* priority
* status
* created_by
* reviewer_id
* created_at
* updated_at

### Review Actions

* id
* request_id
* action
* comments
* reviewed_by
* reviewed_at

---

# 🔄 Request Lifecycle

The system enforces the following state transitions:

```text
PENDING
 ├──> APPROVED
 └──> REJECTED
```

Invalid transitions are blocked by the Service Layer.

Examples:

* APPROVED → REJECTED ❌
* REJECTED → APPROVED ❌
* APPROVED → PENDING ❌
* REJECTED → PENDING ❌

---

# ✅ Assessment Requirement Mapping

| Requirement          | Implementation                        |
| -------------------- | ------------------------------------- |
| FastAPI              | REST API Backend                      |
| SQLAlchemy ORM       | Database Access Layer                 |
| PostgreSQL           | Relational Database                   |
| React.js             | Frontend Application                  |
| Vite                 | Build Tool                            |
| React Router         | Client-Side Routing                   |
| Axios                | API Communication                     |
| Google OAuth 2.0     | Authentication                        |
| JWT Session          | Protected Access                      |
| Role-Based Access    | Requester / Reviewer                  |
| Layered Architecture | API → Service → Repository → Database |
| Testing              | Pytest + React Testing Library        |

---

This architecture is designed to be modular, maintainable, testable, and aligned with the requirements of the Csyrus Technologies Engineering Internship Assessment.
