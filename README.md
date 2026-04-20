# PathPilot
A planning app that optimizes a student's degree/certificate path and shows career outcomes (salary ranges, roles), based on the Degree/Certificate Optimizer's rules engine + "salary API" future-work direction.

Need:
- Python 3.11
- Docker Desktop

Setup:
1. Clone the repo
2. Install docker desktop
   
    Follow instructions of installation of Docker for now.

4. Setup your env

   Create a .env file within pathpilot-backend folder:
   
   ``touch pathpilot-backend/.env``

    Copy the example .env.example file in pathpilot-backend
    and put it in the ceated .env file and fill out the information (your Email and your API KEYS) on the example.
    Website to request API keys: 
       https://developer.usajobs.gov/api-reference/
       https://theirstack.com/en/job-posting-api
    
6. Run docker compose up in your terminal

   In vscode open up a terminal, then run:

    ``docker compose up --build``
   
8. Enter http://localhost:5003 in your searchbar (front-end not up yet) 
   Use http://localhost:5001 for testing backend API
