# Real-Time Chat & Task Manager API

A high-performance backend built with FastAPI, featuring real-time WebSocket communication, JWT-based authentication, and a custom sliding-window rate limiter. Fully containerized with Docker and PostgreSQL.

## 🚀 Features

*   **Real-Time WebSockets:** Bi-directional communication for instant messaging and live task updates.
*   **Sliding Window Rate Limiter:** Custom algorithm preventing spam (e.g., max 5 messages per 10 seconds) using highly efficient `collections.deque` structures.
*   **JWT Authentication:** Secure stateless authentication using `PyJWT` with RSA public/private key pairs.
*   **Asynchronous Database:** Non-blocking database operations using SQLAlchemy 2.0, Asyncpg, and PostgreSQL.
*   **Containerized:** One-command deployment using Docker and Docker Compose.

## 🛠️ Tech Stack

*   **Framework:** FastAPI (Python 3.11+)
*   **Database:** PostgreSQL, SQLAlchemy (Async), Alembic (Migrations)
*   **Auth:** PyJWT, Passlib, Bcrypt
*   **Infrastructure:** Docker, Docker Compose

## 📦 Getting Started

### Prerequisites
*   [Docker](https://www.docker.com/get-started) and Docker Compose installed on your machine.
*   Git bash or any terminal.

### 1. Clone the repository
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
```

### 2. Environment Variables
Create a `.env` file in the root directory (next to `docker-compose.yaml`) and add the following:
```ini
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=taskmanager
DATABASE_URL=postgresql+asyncpg://myuser:mypassword@db:5432/taskmanager
```

### 3. Generate Security Certificates
Create a `certs` folder in the root directory and generate your RSA keys for JWT auth:
```bash
mkdir certs
cd certs
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem
cd ..
```

### 4. Run with Docker
Spin up the database and web server in the background:
```bash
docker-compose up -d --build
```

The API will be available at `http://localhost:8000`. 
Check out the interactive Swagger UI documentation at `http://localhost:8000/docs`.

## 🧪 Testing the WebSocket Rate Limiter

You can test the real-time chat and sliding window bouncer using Postman:

1.  Authenticate via the `/login` endpoint to get your JWT token.
2.  Connect to `ws://localhost:8000/ws?token=YOUR_TOKEN`.
3.  Send a JSON message.
4.  **To test the bouncer:** Send 6 messages in under 10 seconds. The server will drop the 6th message and return a rate limit error without crashing the connection.

## 🗄️ Database Migrations
To run Alembic migrations inside the running Docker container:
```bash
docker-compose exec web alembic upgrade head
```