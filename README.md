# PathPilot
A planning app that optimizes a student's degree/certificate path and shows career outcomes (salary ranges, roles), based on the Degree/Certificate Optimizer's rules engine + "salary API" future-work direction.

Need:
- Python 3.11
- Docker Desktop

Setup:
1. Clone the repo
2. Install docker desktop
3. Setup your env

    copy the example .env file in pathpilot-backend
    create a new .env file and fill out based on the example.
    Website to request API keys: 
       https://developer.usajobs.gov/api-reference/
       https://theirstack.com/en/job-posting-api
    
4. Run docker compose up in your terminal
5. Enter http://localhost:5003 in your searchbar (front-end not up yet) 
   Use http://localhost:5001 for testing backend API
