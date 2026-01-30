Patient Encounter Management System

This is a backend application built using FastAPI, SQLAlchemy, and MySQL.
It manages patients, doctors, and appointment scheduling with proper
business rules and testing.

--------------------------------------------------

FEATURES

- Create and view patients
- Create and view doctors
- Schedule appointments
- Prevent overlapping appointments for doctors
- Appointments must be in the future
- Timezone-aware datetime validation
- Retrieve appointments by date
- Automated tests with coverage
- CI pipeline using GitHub Actions

--------------------------------------------------

TECH STACK

- FastAPI
- SQLAlchemy
- MySQL (SQLite used for testing)
- Pydantic v2
- Pytest
- GitHub Actions
- Poetry

--------------------------------------------------

PROJECT STRUCTURE

patient-encounter-system
|
|-- src
|   |-- main.py
|   |-- database.py
|   |-- models
|   |-- schemas
|   |-- services
|
|-- tests
|-- .github/workflows/ci.yml
|-- pyproject.toml
|-- requirements.txt
|-- README.md

--------------------------------------------------

SETUP INSTRUCTIONS

1. Clone the repository

   git clone <your-repo-url>
   cd patient-encounter-system

2. Install dependencies

   poetry install

3. Create .env file

   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=your_username
   DB_PASSWORD=your_password
   DB_NAME=your_database

4. Run the application

   poetry run uvicorn src.main:app --reload

5. Open Swagger UI

   http://127.0.0.1:8000/docs

--------------------------------------------------

RUNNING TESTS

Run tests with coverage:

   poetry run pytest --cov=src

All tests pass with coverage above 90 percent.

--------------------------------------------------

API ENDPOINTS

Patients
- POST /patients
- GET /patients/{id}

Doctors
- POST /doctors
- GET /doctors/{id}

Appointments
- POST /appointments
- GET /appointments?date=YYYY-MM-DD&doctor_id=

--------------------------------------------------

BUSINESS RULES

- Appointments must be timezone-aware
- Appointments must be scheduled in the future
- Doctors cannot have overlapping appointments
- Inactive doctors cannot receive appointments
- Appointment end time is derived and not stored
- Business logic is implemented in the service layer

--------------------------------------------------

CI PIPELINE

GitHub Actions is used to:
- Run linting
- Run formatting checks
- Run security scans
- Run tests with coverage

