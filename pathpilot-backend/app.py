from flask import Flask, jsonify, request
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return "PathPilot web-app is running"

@app.route("/jobs", methods=["GET"])
def jobs():
    keyword = request.args.get("keyword", "")
    try:
        # usajobs api call
        usajobs_response = requests.get(
            "https://data.usajobs.gov/api/search", 
            headers = {
                "User-Agent": os.getenv("USAJOBS_EMAIL"),
                "Authorization-Key": os.getenv("USAJOBS_API_KEY")
            },
            params={
                "Keyword": keyword,
                "ResultsPerPage": 10
            }
        )
        usajobs_data = usajobs_response.json()
    except Exception as e:
        usajobs_data = {"error": f"USAJobs API failed: {str(e)}"}

    # theirstack api call
    try:
        theirstack_response = requests.get(
            "https://api.theirstack.com/...",
            headers = {
                "Authorization": os.getenv("THEIRSTACK_API_KEY")
            },
            params = {
                "keyword": keyword
            }
        )
        theirstack_data = theirstack_response.json()
    except Exception as e:
        theirstack_data = {"error": f"TheirStack API failed: {str(e)}"}
    return jsonify({
        "federal_jobs": usajobs_data,
        "private_jobs": theirstack_data
    })

# do not change the host (specific to Docker)
# allows Flask to accept connections from anywhere including Docker's internals.

# port number you can change as long as it's also retroactively changed in the docker-compose.yml
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)