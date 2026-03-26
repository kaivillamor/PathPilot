from flask import Blueprint, jsonify, request
from services.usajobs import get_usajobs
from services.theirstack import get_theirstack

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

@jobs_bp.route("/jobs", methods=["GET"])
def jobs():
    degree = request.args.get('degree', '')

    if not degree:
        return jsonify({"error": "No degree has been selected"}), 400
    usajobs_series = USAJOBS_DEGREE_MAPPING.get(degree, degree)
    theirstack_title = THEIRSTACK_DEGREE_MAPPING.get(degree, degree)

    if isinstance(theirstack_title, str):
        theirstack_title = [theirstack_title]

    usajobs_data = get_usajobs(usajobs_series)
    theirstack_data = get_theirstack(theirstack_title)

    return jsonify({
        "degree": degree,
        "federal_jobs": usajobs_data,
        "private_jobs": theirstack_data
    })