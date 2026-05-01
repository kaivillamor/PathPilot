from flask import Flask, jsonify, request
from dotenv import load_dotenv
from routes.jobs import jobs_bp
from metrics import get_metrics, init_db
import os

load_dotenv()

app = Flask(__name__)

app.register_blueprint(jobs_bp)

init_db()

@app.route("/")
def home():
    return jsonify({"error": "Unauthorized"}), 403

@app.route("/metrics")
def metrics():
    secret = os.getenv("METRICS_SECRET")
    if secret and request.headers.get("X-Metrics-Secret") != secret:
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify(get_metrics())

# do not change the host (specific to Docker)
# allows Flask to accept connections from anywhere including Docker's internals.

# port number you can change as long as it's also retroactively changed in the docker-compose.yml
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)