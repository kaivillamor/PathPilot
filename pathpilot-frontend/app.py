from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import os

app = Flask(__name__)

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:5000")
METRICS_SECRET = os.getenv("METRICS_SECRET", "")

limiter = Limiter(get_remote_address, app=app, default_limits=[])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/roadmap", methods=["GET", "POST"])
@limiter.limit("5 per 12 hours")
def roadmap():
    if request.method == "GET":
        return render_template("roadmap.html")
    degree = request.form.get("degree", "")
    year = request.form.get("year", "")
    interests = request.form.get("interests", "")
    try:
        # generous, the backend waits on an openai call, but under gunicorn's 60s
        response = requests.post(f"{BACKEND_URL}/roadmap", json={"degree": degree, "year": year, "interests": interests}, headers={"X-Metrics-Secret": METRICS_SECRET}, timeout=45)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return render_template("roadmap.html", error=str(e), degree=degree, year=year, interests=interests)
    return render_template("roadmap.html", roadmap=data, degree=degree, year=year, interests=interests)

@app.route("/results")
def results():
    degree = request.args.get("degree")
    try:
        # the backend calls two apis at timeout=10 each, so allow for both
        response = requests.get(f"{BACKEND_URL}/jobs", params={"degree": degree}, timeout=30)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return render_template("results.html", error=str(e))
    return render_template("results.html", federal_jobs=data["federal_jobs"], private_jobs=data["private_jobs"], degree=degree)
# only used for local runs, gunicorn serves this in the container.
# debug must stay off in production: it exposes the Werkzeug console
if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    app.run(debug=debug, host="0.0.0.0", port=5000)