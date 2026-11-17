# Salon Appointment API

A role-based REST API for salon service catalogues, staff and appointment booking, built with Flask, SQLAlchemy and JWT, with a React front end that also runs in a no-backend demo mode.

- **Live Demo:** _add your deployed frontend URL here_ (runs on mock data, see [note](#about-the-live-demo))
- **API docs:** interactive Swagger UI at `/swagger` when the API is running
- **Frontend repo:** https://github.com/mungaiDaniel/Salon-Appointment-UI

![Screenshot or GIF placeholder](docs/screenshot.png)

## Features

- **JWT authentication** with access and refresh tokens; roles `user < admin < super_admin` checked on every request against the database, so promotions and deletions take effect immediately
- **Secure by default:** authorization fails closed, scrypt password hashing (legacy md5-crypt hashes are upgraded transparently at login), no password hashes in any response, rate-limited login and registration, CORS limited to configured origins
- **Input validation** with Marshmallow, returning `422` with per-field details
- **One consistent error format** with stable machine-readable codes (`{"status", "code", "message", "details"}`) for every failure, including 404/405/500
- **Booking integrity:** customers only see their own bookings, and an employee cannot be double-booked for the same slot (`409`, enforced by a unique constraint as well as an up-front check)
- **Service catalogue and staff assignment** (which employee performs which service)
- **Operational basics:** health endpoint with DB check, structured JSON logging, Alembic migrations, a `flask create-admin` command, Docker and Compose setup
- **Quality gates:** 84 pytest tests at 99% coverage (CI fails under 90%), black, flake8, and `pip-audit` in CI

## Tech stack

**Backend:** Python 3.12+, Flask 3, Flask-SQLAlchemy / SQLAlchemy 2, Flask-JWT-Extended, Marshmallow 4, Flask-Migrate (Alembic), Flask-Limiter, Flask-CORS, Swagger UI, PostgreSQL (SQLite for dev and tests), Gunicorn, Docker

**Frontend:** React 18, MUI 5, Bootstrap 5, axios, React Router 6, Jest and Testing Library

## Architecture

```mermaid
flowchart LR
    UI["React SPA<br/>(demo mode: in-memory mock API)"] -- "HTTPS + JWT" --> API
    subgraph API["Flask API (create_app factory)"]
        V["Blueprints / views<br/>(auth, service, assistances, bookings)"] --> C["Controllers<br/>business rules"]
        C --> M["SQLAlchemy models"]
        V -. validates .-> S["Marshmallow schemas"]
        V -. guards .-> D["role_required<br/>(JWT + DB role)"]
        E["Central error handler"]
    end
    M --> DB[("PostgreSQL / SQLite")]
```

```
app/
  auth/ service/ assistances/ bookings/   # each: model.py, controllers.py, views.py
  schemas/        # Marshmallow input + output schemas
  utils/          # role_required decorator
  errors.py       # ApiError + central JSON error handlers
  extensions.py   # db, jwt, limiter, cors, migrate
  cli.py          # flask create-admin
config.py         # Development / Production / Testing configs (env-driven)
main.py           # application factory; wsgi.py is the gunicorn entrypoint
migrations/       # Alembic
tests/            # pytest suite
```

Views stay thin (parse, validate, serialise); controllers hold the business rules and raise `ApiError`s that the central handler turns into responses.

## API endpoints

Base path `/api/v1`. Roles are cumulative (`admin` includes `user`; `super_admin` includes both). Full schemas are in Swagger UI.

| Method | Route | Description | Auth |
|---|---|---|---|
| POST | `/users` | Register a customer account | No |
| POST | `/login` | Log in, returns access and refresh tokens | No |
| POST | `/refresh` | New access token from a refresh token | Refresh token |
| GET | `/users` | List all users | admin |
| GET | `/users/{id}` | Get a profile (own, or any as admin) | Yes |
| PUT | `/admin/{id}` | Promote a user to admin | super_admin |
| PUT | `/super_admin/{id}` | Promote a user to super_admin | super_admin |
| GET | `/employees` | Staff list (contact details only for admin callers) | No |
| GET | `/stylings` | List services | No |
| GET | `/stylings/{id}` | Get a service | No |
| POST | `/stylings` | Create a service | admin |
| PUT | `/stylings/{id}` | Replace a service | admin |
| DELETE | `/stylings/{id}` | Delete a service | admin |
| POST | `/employee/{user_id}/{service_id}` | Assign a service to an employee | admin |
| GET | `/employee/{user_id}` | Service assignments for an employee | No |
| GET | `/employee_service/{employee_id}` | Full service records an employee performs | No |
| POST | `/booking` | Book an appointment (as the authenticated user) | Yes |
| GET | `/booking` | List bookings (all for admins, own for customers) | Yes |
| GET | `/booking/{id}` | Get a booking (owner or admin) | Yes |
| GET | `/health` (also `/api/v1/health`) | Liveness and database check | No |

## Local setup

### Backend

```bash
git clone https://github.com/mungaiDaniel/Salon-Appointment-Api.git
cd Salon-Appointment-Api
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

cp .env.example .env
# set SECRET_KEY in .env (>= 32 chars):
python -c "import secrets; print(secrets.token_hex(32))"

flask db upgrade                                 # creates the SQLite dev DB (or your DATABASE_URI)
flask create-admin you@example.com               # prompts for a password; creates the first super admin
flask run                                        # http://localhost:5000  (Swagger UI at /swagger)
```

The API will not start without a `SECRET_KEY` of at least 32 characters. Environment variables are documented in [`.env.example`](.env.example): `DATABASE_URI`, `CORS_ORIGINS`, JWT lifetimes, rate limits.

**PostgreSQL:** set `DATABASE_URI=postgresql://user:password@localhost:5432/salon_db` and run `flask db upgrade`.

**Docker:** `cp .env.example .env`, fill in `SECRET_KEY` and `POSTGRES_PASSWORD`, then `docker compose up --build`. The container applies migrations on start.

### Frontend

```bash
git clone https://github.com/mungaiDaniel/Salon-Appointment-UI.git
cd Salon-Appointment-UI
npm install --legacy-peer-deps
cp .env.example .env           # REACT_APP_API_URL=http://localhost:5000/api/v1
npm start                      # http://localhost:3000
```

Add `http://localhost:3000` to `CORS_ORIGINS` on the API (it is the default). To try the UI without any backend, run `npm run start:demo`.

### Running the tests

```bash
pytest                  # 84 tests; fails if coverage drops below 90%
black --check . && flake8
pip-audit -r requirements.txt
```

## About the live demo

The hosted demo is the **frontend only**, deployed with `REACT_APP_DEMO_MODE=true`. Every API call is answered by an in-memory mock with clearly fake sample data, so changes are not saved and reset on reload. The real Flask backend in this repository is not hosted for the demo; run it locally using the steps above to use the real API.

## Author

**Daniel Mungai** — backend developer (Python / Flask)

- GitHub: [github.com/mungaiDaniel](https://github.com/mungaiDaniel)
- LinkedIn: [linkedin.com/in/daniel-mungai-7a52451b8](https://linkedin.com/in/daniel-mungai-7a52451b8)
