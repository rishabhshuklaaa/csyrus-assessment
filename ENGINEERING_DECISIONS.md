# Engineering Decisions & Architecture Rationale

This document outlines the core architectural choices, design patterns, and technical trade-offs made during the development of the Csyrus Workflow Approval Management System. It also maps the implementation directly to the assessment requirements.

## 🏗️ Architecture Choices and Rationale

The application follows a decoupled client-server architecture, separating the presentation layer from the business logic and data layers.

* **Backend (FastAPI & Python 3.x):** FastAPI was selected for its exceptional performance, automatic OpenAPI documentation generation, and strict type safety. By natively integrating with Pydantic, the framework provides automatic data validation at the API boundary, which drastically reduces runtime errors and significantly boosts developer productivity.
* **Layered Backend Design:** The backend code is structured into discrete layers: `Routers` (API endpoints) -> `Services` (Business Logic) -> `Repositories` (Database Operations) -> `Models` (Data Schema). This separation of concerns makes the codebase modular, highly testable, and easy to maintain.
* **Frontend (React.js & Vite):** React was chosen for its efficient virtual DOM and component-driven architecture. Vite was selected as the build tool over Webpack due to its drastically faster Hot Module Replacement (HMR) and optimized build times, providing a superior developer experience.

## 🛡️ Auth Design Decisions

Authentication is strictly implemented using **Google OAuth 2.0** combined with **JSON Web Tokens (JWT)**. Standard email/password login is intentionally omitted to meet security requirements.

* **Delegated Security:** By relying on Google OAuth, the system avoids handling and storing highly sensitive credentials (like password hashes), mitigating risks associated with data breaches.
* **HttpOnly Cookie Authentication:** Upon successful OAuth callback, the backend issues a signed JWT and sets it as an `HttpOnly` cookie. This is a crucial security decision that prevents Cross-Site Scripting (XSS) attacks from accessing the token via JavaScript.
* **Axios Interceptors:** On the frontend, Axios is configured with `withCredentials: true`. This ensures that the browser automatically includes the secure `HttpOnly` JWT cookie with every cross-origin request to the API, completely eliminating the need to manually manage or attach tokens in `Authorization` headers.

## 🗄️ Database Design Decisions

A robust relational database approach was mandated and implemented using **PostgreSQL**.

* **ACID Compliance & SQLAlchemy ORM:** A workflow approval system handles critical state changes. PostgreSQL guarantees ACID compliance, ensuring data consistency. Synchronous SQLAlchemy ORM is used to abstract raw SQL queries into Pythonic objects, providing an inherent defense against SQL injection attacks and simplifying complex table relationships.
* **Alembic Migrations:** Database schemas evolve over time. Alembic is integrated to provide version control for the database, allowing schema upgrades and rollbacks safely across different environments.
* **UUID Primary Keys:** Instead of auto-incrementing integers, UUIDs (`uuid4`) are used for primary keys across all tables. This prevents ID enumeration attacks (where a malicious user might guess another user's sequential request ID) and ensures global uniqueness.

## 🧪 Testing Strategy

The testing philosophy focuses on validating business rules, component isolation, and predictable outcomes.

* **Backend (Pytest):** The backend testing strategy comprehensively validates the API routes and application logic. Tests cover the authentication flow, strict business rules, the complete request lifecycle (creation to resolution), reviewer actions, and valid status transitions (e.g., ensuring a `PENDING` request correctly transitions to `APPROVED` or `REJECTED`).
* **Frontend (Vitest & React Testing Library):** Tests are written to simulate user interactions. External dependencies, such as the `useAuth` hook and the `apiClient` (Axios), are strictly mocked. This ensures that React components are tested in complete isolation without relying on actual network requests or backend state.

## ⚖️ Trade-offs Accepted

* **React Context vs. Global State Libraries:** React's native Context API was used for global state management (Authentication state). While a library like Redux offers better debugging tools, Context is lightweight and fully sufficient for managing standard user sessions, saving development overhead and reducing bundle size.
* **Synchronous Database Operations:** The application utilizes synchronous SQLAlchemy (`psycopg2-binary`). While asynchronous database drivers can handle higher I/O concurrency, the synchronous approach greatly simplifies debugging, transaction management, and test setup, which is ideal for the scale of this assessment.

## 🔮 What I'd Improve with More Time

Given additional time, I would implement the following enhancements:

1.  **Pagination and Filtering:** As the `requests` table grows, fetching all records at once will bottleneck performance. I would implement limit-offset pagination in the FastAPI endpoints and corresponding pagination controls in React.
2.  **Rate Limiting:** Implement rate limiting (e.g., `slowapi`) on the FastAPI backend to protect the API from brute-force hits, particularly on the authentication and request-creation endpoints.
3.  **Audit Logging:** Create a dedicated `audit_logs` table to track every status change, recording the `timestamp`, `user_id`, and `action` for compliance tracking and historical debugging.

---

## ✅ Assessment Compliance

This project was built to strictly align with the mandated requirements of the Csyrus Technologies Engineering Internship Assessment:

* **FastAPI:** Core backend framework utilized for all RESTful API routes.
* **SQLAlchemy ORM:** Used for all database models, relations, and query abstractions.
* **PostgreSQL:** Primary relational database managing users and approval requests.
* **React:** Core frontend UI library.
* **Vite:** Frontend build tool and development server.
* **React Router:** Handles client-side navigation between dashboard, forms, and login views.
* **Axios:** Configured HTTP client handling API requests with `withCredentials=true`.
* **Google OAuth 2.0:** Sole authentication provider. Email/password login is completely disabled.
* **JWT Session Authentication:** Stateless sessions managed securely via JWTs.
* **Role-Based Access Control (RBAC):** Distinct roles (`Requester` and `Reviewer`) strictly enforced at the API and UI levels.
* **Pytest:** Backend testing framework ensuring API reliability and business logic validation.
* **React Testing Library / Vitest:** Frontend testing stack verifying component rendering and isolation.
* **Documentation:** Comprehensive `README.md`, `ENGINEERING_DECISIONS.md`, and `COLLABORATION.md` provided.
* **Git Workflow:** Version control maintained throughout the development lifecycle.