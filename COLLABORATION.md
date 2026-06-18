# Collaboration & Deployment Considerations

This document outlines the assumptions made during development, current system limitations, and the necessary architectural shifts required to transition this application from a local development environment to a live, scalable production system.

## 🤔 Assumptions Made

* **Role Provisioning:** It is assumed that any user logging in via Google OAuth is initially provisioned as a `Requester`. Elevation to the `Reviewer` role is handled administratively at the database level, as a dedicated Admin UI was outside the scope of this assessment.
* **Client Environment:** Users will interact with the application via modern, JavaScript-enabled web browsers that fully support Cross-Origin Resource Sharing (CORS) and `HttpOnly` cookie storage.
* **Workflow Linearity:** The approval lifecycle is assumed to be linear (`PENDING` → `APPROVED` or `REJECTED`). Complex multi-stage or parallel approvals are not currently modeled in the database schema.

## 🚧 Known Limitations

* **Lack of Real-Time Updates:** The system currently relies on standard HTTP request-response cycles. If a Reviewer approves a request, the Requester will not see the updated status until they manually refresh their dashboard.
* **No Email Notifications:** The system does not currently integrate with an SMTP service (e.g., SendGrid or AWS SES) to notify users of status changes or new assignments.
* **Attachment Support:** The schema is strictly text-based. Binary file uploads (e.g., PDF justifications or image attachments) for requests are not supported.
* **Synchronous I/O Blocking:** Because the backend utilizes synchronous SQLAlchemy, highly concurrent database transactions could potentially block the event loop, unlike a fully asynchronous driver.

## 🏭 What Would Change in Production

If this application were deployed to a live production environment, the following structural and infrastructural changes would be implemented:

1. **Process Management:** The development server (`uvicorn main:app --reload`) would be replaced with a robust process manager like **Gunicorn** utilizing Uvicorn worker classes (`gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`) to maximize CPU core utilization and ensure crash recovery.
2. **Containerization & Orchestration:** Both the FastAPI backend and the React frontend (served via Nginx) would be containerized using **Docker**. This guarantees environment parity across staging and production.
3. **CI/CD Integration:** Implementation of GitHub Actions pipelines to automatically trigger the Pytest and Vitest suites, run linting (Ruff/ESLint), and execute Alembic database migrations before deploying to cloud infrastructure.
4. **Strict CORS & TLS:** CORS origins would be strictly locked down to the production frontend domain. Furthermore, TLS (HTTPS) would be enforced, which is absolutely mandatory for secure `HttpOnly` cookie transmission (`Secure=True`).
5. **Database Connection Pooling:** While SQLAlchemy handles internal pooling, deploying multiple load-balanced FastAPI instances would quickly exhaust PostgreSQL's maximum connections. I would deploy **PgBouncer** in transaction-pooling mode to efficiently manage connections.

## 📈 Scalability Considerations

As organizational traffic and the volume of requests increase, the architecture is primed to scale effectively:

* **Horizontal Scaling (Statelessness):** Because authentication is handled entirely via JWTs stored in client-side cookies, the FastAPI backend is 100% stateless. We can spin up multiple backend instances behind an Application Load Balancer (ALB) without worrying about session affinity or desync.
* **Database Indexing:** To ensure read operations remain performant as the `approval_requests` table grows, composite indexes would be necessary. For example, indexing `(created_by, status)` ensures that a Requester fetching their specific pending dashboard loads instantly.
* **Caching Layer:** For frequently accessed but rarely changed data (e.g., fetching the current user's profile or static dropdown options), a **Redis** caching layer could be introduced to intercept requests before they hit PostgreSQL, significantly reducing database load.
* **Read Replicas:** If the system becomes heavily read-intensive (e.g., Reviewers constantly filtering and searching through historical requests), PostgreSQL read replicas could be deployed, routing read queries to the replicas and keeping the primary database dedicated to write operations (approvals/creations).