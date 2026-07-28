from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

# must run before the blueprints are imported, they read env vars on import
load_dotenv()

from routes.jobs import jobs_bp
from routes.roadmap import roadmap_bp
from metrics import get_metrics, init_db

app = Flask(__name__)

app.register_blueprint(jobs_bp)
app.register_blueprint(roadmap_bp)

init_db()

@app.route("/")
def home():
    return jsonify({"error": "Unauthorized"}), 403

@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"})

@app.route("/metrics")
def metrics():
    secret = os.getenv("METRICS_SECRET")
    if secret and request.headers.get("X-Metrics-Secret") != secret:
        return jsonify({"error": "Unauthorized"}), 403
    try:
        return jsonify(get_metrics())
    except Exception as e:
        return jsonify({"error": f"metrics unavailable: {e}"}), 503

# do not change the host (specific to Docker)
# allows Flask to accept connections from anywhere including Docker's internals.

# defaults to 5000 for docker-compose, Railway injects its own PORT
if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    app.run(debug=debug, host="0.0.0.0", port=port)