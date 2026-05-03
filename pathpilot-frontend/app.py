import time
from copy import deepcopy
from typing import Any

from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

DEFAULT_CATALOG = {
    "institutions": [
        {"key": "pathpilot_demo", "label": "PathPilot Demo University"},
        {"key": "northeast_state", "label": "Northeast State College"},
        {"key": "pacific_tech", "label": "Pacific Tech Institute"},
    ],
    "degrees": [
        "Computer Science",
        "Cybersecurity",
        "Information Technology",
        "Computer Engineering",
        "Data Science",
        "Business Administration",
        "Marketing",
        "Product Management",
    ],
    "courses": [],
}

CATALOG_CACHE_TTL_SECONDS = 300
CATALOG_CACHE: dict[str, Any] = {"data": None, "loaded_at": 0.0}


def clone_default_catalog():
    return deepcopy(DEFAULT_CATALOG)


def normalize_catalog(raw_catalog):
    catalog = clone_default_catalog()
    if not isinstance(raw_catalog, dict):
        return catalog
    for key in ("institutions", "degrees", "courses"):
        value = raw_catalog.get(key)
        if isinstance(value, list):
            catalog[key] = value
    return catalog


def fetch_catalog_from_backend():
    response = requests.get("http://backend:5000/planner/catalog", timeout=10)
    response.raise_for_status()
    return response.json()


def get_catalog():
    now = time.time()
    cached = CATALOG_CACHE.get("data")
    loaded_at = CATALOG_CACHE.get("loaded_at", 0.0)
    if cached and (now - loaded_at) < CATALOG_CACHE_TTL_SECONDS:
        return cached

    catalog = clone_default_catalog()
    try:
        backend_catalog = fetch_catalog_from_backend()
        catalog = normalize_catalog(backend_catalog)
    except Exception as exc:
        app.logger.warning("Unable to load catalog from backend: %s", exc)
        if cached:
            # Use stale cache instead of dropping all options on transient failures.
            return cached
    CATALOG_CACHE["data"] = catalog
    CATALOG_CACHE["loaded_at"] = now
    return catalog


def parse_selected_courses(args):
    normalized = []
    seen = set()
    for code in args.getlist("courses"):
        code_norm = str(code).strip().upper()
        if code_norm and code_norm not in seen:
            seen.add(code_norm)
            normalized.append(code_norm)
    return normalized


@app.route("/")
def index():
    catalog = get_catalog()
    return render_template("index.html", catalog=catalog)


@app.route("/results")
def results():
    degree = request.args.get("degree")
    institution = request.args.get("institution", "pathpilot_demo")
    job_match_mode = request.args.get("job_match_mode", "strong")
    if job_match_mode not in {"all", "strong"}:
        job_match_mode = "strong"
    try:
        min_match_score = int(request.args.get("min_match_score", 1))
    except (TypeError, ValueError):
        min_match_score = 1
    min_match_score = max(1, min(min_match_score, 10))
    if not degree:
        return render_template("results.html", error="Please choose a degree before searching.")

    completed_courses = parse_selected_courses(request.args)
    if not completed_courses:
        return render_template(
            "results.html",
            error="Please select at least one completed course before viewing job results.",
            degree=degree,
            selected_course_count=0,
            plan={"skill_profile": [], "unrecognized_course_codes": []},
            federal_jobs=[],
            private_jobs=[],
        )
    try:
        response = requests.get(
            "http://backend:5000/jobs",
            params={
                "degree": degree,
                "institution": institution,
                "courses": completed_courses,
                "job_match_mode": job_match_mode,
                "min_match_score": min_match_score,
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
    except Exception as exc:
        app.logger.warning("Failed to fetch jobs for degree '%s': %s", degree, exc)
        return render_template("results.html", error=str(exc))
    return render_template(
        "results.html",
        federal_jobs=data["federal_jobs"],
        private_jobs=data["private_jobs"],
        degree=degree,
        selected_institution=institution,
        job_match_mode=data.get("job_match_mode", "all"),
        min_match_score=data.get("min_match_score", min_match_score),
        selected_course_count=len(completed_courses),
        selected_courses=completed_courses,
        plan=data.get("plan"),
    )


@app.route("/course-options")
def course_options():
    institution = request.args.get("institution", "pathpilot_demo")
    degree = request.args.get("degree", "")
    try:
        response = requests.get(
            "http://backend:5000/planner/catalog",
            params={"institution": institution, "degree": degree},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return jsonify({"courses": data.get("courses", [])})
    except Exception as exc:
        app.logger.warning(
            "Failed to load course options for institution '%s', degree '%s': %s",
            institution,
            degree,
            exc,
        )
        return jsonify({"courses": []})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
