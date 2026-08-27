# Salon Appointment API

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask%202.x-lightgrey)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/database-PostgreSQL%20%7C%20SQLite-blue)](https://www.postgresql.org/)
[![Tests](https://img.shields.io/badge/tests-54%20passed%20%2F%2093%25%20coverage-brightgreen)](#running-automated-tests)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A production-ready RESTful API for salon management and appointment scheduling. Built with **Flask**, **Flask-SQLAlchemy**, **Flask-JWT-Extended**, and **Swagger UI** for documentation. The application provides role-based access control (Customers, Employees, Admins, Super Admins), salon style catalog management, service assignment, and appointment bookings.

---

## Key Features

- **Authentication & Role-Based Access Control**:
  - Secure password hashing (`passlib` / Werkzeug).
  - JWT Access Token & Refresh Token authorization.
  - Role hierarchy: `user`, `admin`, `super_admin`.
- **Salon Service Catalog**:
  - CRUD operations for salon styling services (name, description, cost, duration).
  - Role-protected modifications (admin/super-admin permissions).
- **Appointment Booking System**:
  - Book styling appointments with assigned employees/stylists.
  - Query user bookings and appointment schedules.
- **Employee & Assistance Management**:
  - Link employees with specific salon services.
  - Promote users to employee/admin roles.
- **Monitoring & API Specs**:
  - Health check endpoints (`/health` and `/api/v1/health`) with DB connectivity verification.
  - Structured JSON logging.
  - Interactive Swagger UI documentation at `/swagger`.
- **Fully Self-Contained & Testable**:
  - 54 automated unit/integration tests with 93% code coverage.
  - Coverage gate enforced at ≥70% in CI.
  - Code formatting enforced with `black` and linting with `flake8`.
  - Complete Docker containerization (`Dockerfile` and `docker-compose.yml`).

---

## Project Structure

```
.
├── app/
│   ├── assistances/     # Employee assistance assignment views & controllers
│   ├── auth/            # Authentication, registration & user controllers
│   ├── bookings/        # Appointment booking controllers & views
│   ├── database/        # Database initialization instance
│   ├── logging_config.py # Structured JSON logging configuration
│   ├── schemas/         # Marshmallow serialization schemas
│   ├── service/         # Hair salon styling services catalog
│   └── utils/           # Decorators, JWT helpers & custom HTTP responses
├── tests/               # Pytest suite (conftest fixtures, unit & integration tests)
├── Test/                # unittest-based test suite
├── static/              # Static assets & Swagger specification
├── base_model.py        # Abstract SQLAlchemy base model
├── config.py            # Development, Testing, and Production configurations
├── main.py              # Application entrypoint & Flask factory
├── Dockerfile           # Container build
├── docker-compose.yml   # Orchestration (Web API + PostgreSQL DB)
├── .env.example         # Environment variable template
├── pyproject.toml       # Black formatter configuration
├── .flake8              # Flake8 linter configuration
├── pytest.ini           # Pytest runner configuration
├── requirements.txt     # Pinned Python package dependencies
├── requirements.in      # Unpinned dependency source
└── README.md            # Repository documentation
```

---

## Quickstart Guide

### Prerequisites

- Python 3.10+ **or** Docker

### 1. Local Setup

```bash
# Clone the repository
git clone <repository-url>
cd Salon-Appointment-Api

# Create and activate virtual environment
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Set required environment variables
cp .env.example .env
# Edit .env and set SECRET_KEY and DATABASE_URI

# Run the application
python main.py
```

The server starts at `http://localhost:5000`. Swagger documentation is at `http://localhost:5000/swagger`.

---

### 2. Running Automated Tests

```bash
# Run all tests
python -m pytest

# Run tests with coverage report
coverage run -m pytest
coverage report --fail-under=70
```

Expected output:
```text
54 passed, 93% coverage
```

---

### 3. Code Formatting & Linting

```bash
# Check formatting (no changes)
black --check .

# Auto-format
black .

# Lint
flake8 .
```

---

### 4. Docker Containerization

Run the API and PostgreSQL database in containerized isolation:

```bash
# Copy environment template
cp .env.example .env

# Build and start services
docker compose up --build

# Run tests inside container
docker compose run --rm web pytest

# Run tests with coverage inside container
docker compose run --rm web sh -c "coverage run -m pytest && coverage report"
```

---

## API Endpoints Reference

| Endpoint | Method | Auth Required | Description |
| :--- | :---: | :---: | :--- |
| `/health` | `GET` | No | Health check with DB connectivity |
| `/api/v1/health` | `GET` | No | Health check (API versioned) |
| `/api/v1/users` | `POST` | No | Register a new user |
| `/api/v1/login` | `POST` | No | Authenticate user & receive JWT tokens |
| `/api/v1/users` | `GET` | No | List all registered users |
| `/api/v1/users/<id>` | `GET` | No | Get specific user details |
| `/api/v1/employees` | `GET` | No | List salon employees |
| `/api/v1/admin/<id>` | `PUT` | No | Promote user to admin |
| `/api/v1/super_admin/<id>` | `PUT` | No | Promote user to super admin |
| `/api/v1/stylings` | `GET` | No | List available styling services |
| `/api/v1/stylings/<id>` | `GET` | No | Get styling service details |
| `/api/v1/stylings` | `POST` | Bearer Token | Create new styling service |
| `/api/v1/stylings/<id>` | `PUT` | Bearer Token | Update styling service |
| `/api/v1/stylings/<id>` | `DELETE` | Bearer Token | Delete styling service |
| `/api/v1/booking` | `POST` | Bearer Token | Book a salon appointment |
| `/api/v1/booking` | `GET` | No | List all bookings |
| `/api/v1/booking/<id>` | `GET` | No | Get booking details |
| `/api/v1/employee/<uid>/<sid>` | `POST` | No | Assign employee to service |
| `/swagger` | `GET` | No | Interactive Swagger UI |

---

## Environment Variables

| Variable | Default | Description |
| :--- | :--- | :--- |
| `FLASK_CONFIG` | `config.DevelopmentConfig` | Configuration class |
| `DATABASE_URI` | `sqlite:///salon_dev.db` | Database connection string |
| `TEST_DATABASE_URI` | `sqlite:///:memory:` | Test database URI |
| `SECRET_KEY` | *(required)* | JWT & session signing key |
| `PORT` | `5000` | HTTP port |

See [`.env.example`](.env.example) for a complete template.

---

## CI/CD

GitHub Actions runs on every push/PR to `main`/`master`:

1. **Install** — `pip install -r requirements.txt`
2. **Format check** — `black --check .`
3. **Lint** — `flake8 .`
4. **Test + Coverage** — `coverage run -m pytest && coverage report --fail-under=70`

---

## License

MIT License.