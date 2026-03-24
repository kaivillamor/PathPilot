from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "PathPilot web-app is running"

@app.route("/jobs", methods=["GET"])
def jobs():
    keyword = request.args.get("keyword", "")
    
    # usajobs api call
    response = requests.get(
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
    
    # error check
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch"}), response.status_code
    
    return jsonify(response.json())

# do not change the host (specific to Docker)
# allows Flask to accept connections from anywhere including Docker's internals.

# port number you can change as long as it's also retroactively changed in the docker-compose.yml
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)