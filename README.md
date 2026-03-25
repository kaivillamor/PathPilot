# PathPilot
A planning app that optimizes a student's degree/certificate path and shows career outcomes (salary ranges, roles), based on the Degree/Certificate Optimizer's rules engine + "salary API" future-work direction.

Need:
- Python 3.11
- Docker Desktop

Setup:
1. Clone the repo
2. Create the venv

    python -m venv venv
    source venv/bin/activate

3. Install dependencies from requirements

    pip install -r pathpilot-backend/requirements.txt

4. Setup your env

    copy the example .env file in pathpilot-backend
    create a new .env file and fill out based on the example.
    Website to get request API key: https://developer.usajobs.gov/api-reference/