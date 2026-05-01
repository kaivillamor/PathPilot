from flask import Blueprint, jsonify, request
from openai import OpenAI
from metrics import get_db
import os
import json

roadmap_bp = Blueprint("roadmap", __name__)

VALID_DEGREES = {
    "Computer Science", "Cybersecurity", "Information Technology",
    "Computer Engineering", "Data Science", "Business Administration",
    "Marketing", "Product Management"
}
VALID_YEARS = {"Freshman", "Sophomore", "Junior", "Senior"}

@roadmap_bp.route("/roadmap", methods=["POST"])
def roadmap():
    secret = os.getenv("METRICS_SECRET")
    if secret and request.headers.get("X-Metrics-Secret") != secret:
        return jsonify({"error": "Unauthorized"}), 403

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    degree = data.get("degree", "").strip()
    year = data.get("year", "").strip()
    interests = data.get("interests", "").strip()[:500]

    if degree not in VALID_DEGREES:
        return jsonify({"error": "Invalid degree selected"}), 400
    if year not in VALID_YEARS:
        return jsonify({"error": "Invalid year selected"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT code, name, required, elective, mathematics FROM courses WHERE degree = %s ORDER BY code", (degree,))
    courses = cur.fetchall()
    cur.close()
    conn.close()

    interests_line = f" with interests in: {interests}" if interests else ""
    required_courses = [f"- {r[0]}: {r[1]}" for r in courses if r[2]]
    electives = [f"- {r[0]}: {r[1]}" for r in courses if r[3]]
    math_courses = [f"- {r[0]}: {r[1]}" for r in courses if r[4]]
    courses_section = ""
    if required_courses or electives or math_courses:
        courses_section = "\n\nAvailable courses for this degree:"
        if required_courses:
            courses_section += "\nRequired:\n" + "\n".join(required_courses)
        if math_courses:
            courses_section += "\nMathematics:\n" + "\n".join(math_courses)
        if electives:
            courses_section += "\nElectives:\n" + "\n".join(electives)

    has_courses = bool(required_courses or electives or math_courses)
    course_instruction = "Use only the provided course list when building the semester plan." if has_courses else f"Generate realistic course names for a typical {degree} curriculum."

    prompt = f"""A {year} student studying {degree}{interests_line}.{courses_section}

Return a JSON object with exactly these keys:
- semester_plan: array of objects with "semester" (e.g. "Fall 2026") and "courses" (array of 4-5 course name strings). Generate only the remaining semesters based on their year. {course_instruction}
- career_paths: array of 3 objects with "title", "description" (2 sentences), and "salary_range" (e.g. "$75k-$110k")
- skills: array of 8-10 skill strings to develop
- job_titles: array of 5 objects with "title" and "salary_range"

Base all recommendations on a realistic {degree} curriculum and current job market."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a career advisor for college students. Always respond with valid JSON only, no extra text."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        max_tokens=1000
    )

    result = json.loads(response.choices[0].message.content)
    return jsonify(result)
