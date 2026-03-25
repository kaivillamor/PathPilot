from flask import Flask, jsonify, request
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

USAJOBS_DEGREE_MAPPING = {
    "Computer Science" : "1550",
    "Cybersecurity": '2210',
    # Note that in federal, cysec and IT share the same series code
    'Information Technology': '2210',
    'Computer Engineering': '0854',
    'Data Science': '1560',
    'Business Administration': '0343',
    'Marketing': '1101',
    'Product Management': '0301'
    }

# Mappings are subject to change based on how real the job titles are
THEIRSTACK_DEGREE_MAPPING = {
    'Computer Science': 'Software Engineer', 
    'Cybersecurity': [
        'Cybersecurity Analyst',
        'Security Analyst',
        'Security Administrator',
        'Cybersecurity Administrator',
        'Ethical Hacker',
        'DevSecOps Engineer',
        'Information Security Analyst',
        'Soc Analyst',
        'Penetration Tester',
        'Security Engineer',
        'Threat Analyst',
    ],
    'Information Technology': [
        'Database Administrator', 
        'System Administrator', 
        'DevOps Engineer', 
        'Network Administrator', 
        'Cloud Administrator', 
        'IT Helpdesk',
        'IT Support',
        'IT Specialist'
        ],
    'Computer Engineering': ['Computer Engineer', 'Hardware Engineer'],
    'Data Science': ['Data Engineer', 'Data Analyst', 'Data Scientist'],
    'Business Administration': [
        'Product Manager', 
        'Business Analyst', 
        'Operations Manager'],
    'Marketing': ['Marketing Manager', 'Marketing Analyst'],
    'Product Management': ['Product Manager', 'Product Owner']
    }

@app.route("/")
def home():
    return "PathPilot web-app is running"

@app.route("/jobs", methods=["GET"])
def jobs():
    degree = request.args.get('degree', '')
    usajobs_series = USAJOBS_DEGREE_MAPPING.get(degree, degree)
    theirstack_title = THEIRSTACK_DEGREE_MAPPING.get(degree, degree)
    if isinstance(theirstack_title, str):
        theirstack_title = [theirstack_title]
    
    try:
        # usajobs api call
        usajobs_response = requests.get(
            "https://data.usajobs.gov/api/search", 
            headers = {
                "User-Agent": os.getenv("USAJOBS_EMAIL"),
                "Authorization-Key": os.getenv("USAJOBS_API_KEY")
            },
            params={
                'JobCategoryCode': usajobs_series,
                "ResultsPerPage": 10
            },
            timeout = 10
        )
        usajobs_data = usajobs_response.json()
    except Exception as e:
        usajobs_data = {"error": f"USAJobs API failed: {str(e)}"}

    # theirstack api call
    try:
        theirstack_response = requests.post(
            "https://api.theirstack.com/v1/jobs/search",
            headers = {
                "Authorization": f"Bearer {os.getenv('THEIRSTACK_API_KEY')}",
                'Content-Type': 'application/json'
            },
            json = {
                'job_title_or': theirstack_title,
                'job_country_code_or': ['US'],
                'posted_at_max_age_days': 30,
                'limit': 10,
                'page': 0
            },
            timeout = 10
        )
        theirstack_data = theirstack_response.json()
    except Exception as e:
        theirstack_data = {"error": f"TheirStack API failed: {str(e)}"}
    return jsonify({
        'degree': degree,
        "federal_jobs": usajobs_data,
        "private_jobs": theirstack_data
    })

# do not change the host (specific to Docker)
# allows Flask to accept connections from anywhere including Docker's internals.

# port number you can change as long as it's also retroactively changed in the docker-compose.yml
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)