from flask import Blueprint, jsonify, request
from services.usajobs import get_usajobs
from services.theirstack import get_theirstack
from services.planner import (
    build_degree_plan,
    get_course_options,
    get_supported_degrees,
    parse_courses_from_query,
    get_supported_institutions,
)
from metrics import log_request, log_error, log_degree_search, log_response_time
import time

jobs_bp = Blueprint("jobs", __name__)

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


def parse_int(value, fallback):
    try:
        parsed = int(value)
        return parsed if parsed >= 0 else fallback
    except (TypeError, ValueError):
        return fallback


def annotate_skill_matches(jobs, skill_keywords):
    if isinstance(jobs, dict):
        return jobs
    keywords = [k.lower() for k in skill_keywords if k]
    annotated = []
    for job in jobs:
        text_fields = [
            "title",
            "summary",
            "job_summary",
            "description",
            "qualification_summary",
            "requirements",
            "skills",
            "company_industry",
        ]
        content = " ".join(
            str(job.get(field, ""))
            for field in text_fields
        ).lower()
        matches = [skill for skill in keywords if skill in content]
        copy = dict(job)
        copy["matched_skills"] = matches
        copy["match_score"] = len(matches)
        annotated.append(copy)
    return annotated


def apply_job_match_mode(jobs, mode, min_score):
    if isinstance(jobs, dict):
        return jobs
    if mode == "strong":
        filtered = [job for job in jobs if job.get("match_score", 0) >= min_score]
        return sorted(filtered, key=lambda job: job.get("match_score", 0), reverse=True)
    return jobs


@jobs_bp.route("/jobs", methods=["GET"])
def jobs():
    start_time = time.time()
    degree = request.args.get('degree', '')
    institution = request.args.get("institution", "pathpilot_demo")

    if not degree:
        return jsonify({"error": "No degree has been selected"}), 400

    completed_courses = parse_courses_from_query(request.args.getlist("courses"))
    transfer_credits = parse_int(request.args.get("transfer_credits", 0), 0)
    max_credits_per_term = parse_int(request.args.get("max_credits_per_term", 12), 12)
    max_credits_per_term = max(3, min(max_credits_per_term, 18))
    job_match_mode = request.args.get("job_match_mode", "all")
    if job_match_mode not in {"all", "strong"}:
        job_match_mode = "all"
    min_match_score = parse_int(request.args.get("min_match_score", 1), 1)
    min_match_score = max(0, min(min_match_score, 10))

    plan = build_degree_plan(
        degree=degree,
        completed_courses=completed_courses,
        transfer_credits=transfer_credits,
        max_credits_per_term=max_credits_per_term,
        institution_key=institution,
    )
    skill_keywords = plan.get("matching_skill_keywords") or [entry["skill"] for entry in plan["skill_profile"]]

    usajobs_series = USAJOBS_DEGREE_MAPPING.get(degree, degree)
    theirstack_title = THEIRSTACK_DEGREE_MAPPING.get(degree, degree)

    if isinstance(theirstack_title, str):
        theirstack_title = [theirstack_title]
    recommended_titles = plan.get("recommended_private_titles", [])
    theirstack_title = list(dict.fromkeys(theirstack_title + recommended_titles))[:12]

    usajobs_data = get_usajobs(usajobs_series)
    theirstack_data = get_theirstack(theirstack_title)
    usajobs_data = annotate_skill_matches(usajobs_data, skill_keywords)
    theirstack_data = annotate_skill_matches(theirstack_data, skill_keywords)
    usajobs_data = apply_job_match_mode(usajobs_data, job_match_mode, min_match_score)
    theirstack_data = apply_job_match_mode(theirstack_data, job_match_mode, min_match_score)

    usajobs_failed = isinstance(usajobs_data, dict) and "error" in usajobs_data
    theirstack_failed = isinstance(theirstack_data, dict) and "error" in theirstack_data
    if usajobs_failed and theirstack_failed:
        log_error("both")
    elif usajobs_failed:
        log_error("usajobs")
    elif theirstack_failed:
        log_error("theirstack")

    log_request()
    log_degree_search(degree)
    log_response_time(time.time() - start_time)
    
    return jsonify({
        "degree": degree,
        "plan": plan,
        "federal_jobs": usajobs_data,
        "private_jobs": theirstack_data,
        "skill_keywords": skill_keywords,
        "institutions": get_supported_institutions(),
        "job_match_mode": job_match_mode,
        "min_match_score": min_match_score,
    })


@jobs_bp.route("/planner/catalog", methods=["GET"])
def planner_catalog():
    institution = request.args.get("institution", "pathpilot_demo")
    degree = request.args.get("degree", "")
    degrees = get_supported_degrees()
    courses = get_course_options(institution, degree) if degree else []
    return jsonify(
        {
            "institution": institution,
            "degree": degree,
            "institutions": get_supported_institutions(),
            "degrees": degrees,
            "courses": courses,
        }
    )
