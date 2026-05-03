from collections import Counter


PROGRAM_TOTAL_CREDITS = 120


COURSE_CATALOG = {
    "CS101": {
        "title": "Intro to Programming",
        "credits": 3,
        "prereqs": [],
        "skills": ["python", "problem solving"],
    },
    "CS120": {
        "title": "Discrete Mathematics",
        "credits": 3,
        "prereqs": [],
        "skills": ["logic", "discrete math"],
    },
    "CS210": {
        "title": "Data Structures",
        "credits": 3,
        "prereqs": ["CS101"],
        "skills": ["algorithms", "data structures"],
    },
    "CS220": {
        "title": "Computer Architecture",
        "credits": 3,
        "prereqs": ["CS101"],
        "skills": ["computer architecture", "debugging"],
    },
    "CS230": {
        "title": "Databases",
        "credits": 3,
        "prereqs": ["CS101"],
        "skills": ["sql", "data modeling"],
    },
    "CS310": {
        "title": "Algorithms",
        "credits": 3,
        "prereqs": ["CS210", "CS120"],
        "skills": ["algorithms", "optimization"],
    },
    "CS330": {
        "title": "Operating Systems",
        "credits": 3,
        "prereqs": ["CS210", "CS220"],
        "skills": ["linux", "operating systems"],
    },
    "CS340": {
        "title": "Software Engineering",
        "credits": 3,
        "prereqs": ["CS210"],
        "skills": ["git", "software testing", "software design"],
    },
    "CS360": {
        "title": "AI Fundamentals",
        "credits": 3,
        "prereqs": ["CS310"],
        "skills": ["machine learning", "python"],
    },
    "CS490": {
        "title": "CS Capstone",
        "credits": 3,
        "prereqs": ["CS310", "CS340"],
        "skills": ["project delivery", "communication"],
    },
    "CY101": {
        "title": "Cybersecurity Fundamentals",
        "credits": 3,
        "prereqs": [],
        "skills": ["cybersecurity", "risk assessment"],
    },
    "CY220": {
        "title": "Network Security",
        "credits": 3,
        "prereqs": ["CY101"],
        "skills": ["network security", "firewalls"],
    },
    "CY230": {
        "title": "Ethical Hacking",
        "credits": 3,
        "prereqs": ["CY101"],
        "skills": ["penetration testing", "vulnerability analysis"],
    },
    "CY310": {
        "title": "Security Operations",
        "credits": 3,
        "prereqs": ["CY220"],
        "skills": ["incident response", "siem"],
    },
    "CY320": {
        "title": "Cloud Security",
        "credits": 3,
        "prereqs": ["CY220"],
        "skills": ["cloud security", "iam"],
    },
    "CY410": {
        "title": "Digital Forensics",
        "credits": 3,
        "prereqs": ["CY310"],
        "skills": ["digital forensics", "incident response"],
    },
    "IT101": {
        "title": "IT Fundamentals",
        "credits": 3,
        "prereqs": [],
        "skills": ["hardware", "troubleshooting"],
    },
    "IT120": {
        "title": "Networking Basics",
        "credits": 3,
        "prereqs": ["IT101"],
        "skills": ["networking", "tcp/ip"],
    },
    "IT220": {
        "title": "Systems Administration",
        "credits": 3,
        "prereqs": ["IT120"],
        "skills": ["linux", "windows", "systems administration"],
    },
    "IT230": {
        "title": "Cloud Administration",
        "credits": 3,
        "prereqs": ["IT120"],
        "skills": ["cloud", "iam"],
    },
    "IT320": {
        "title": "DevOps Foundations",
        "credits": 3,
        "prereqs": ["IT220"],
        "skills": ["ci/cd", "docker", "git"],
    },
    "IT410": {
        "title": "Enterprise IT Operations",
        "credits": 3,
        "prereqs": ["IT220", "IT230"],
        "skills": ["itil", "it service management"],
    },
    "CE101": {
        "title": "Engineering Computing",
        "credits": 3,
        "prereqs": [],
        "skills": ["c", "problem solving"],
    },
    "CE120": {
        "title": "Digital Logic",
        "credits": 3,
        "prereqs": [],
        "skills": ["digital logic", "hardware design"],
    },
    "CE210": {
        "title": "Embedded Systems",
        "credits": 3,
        "prereqs": ["CE101", "CE120"],
        "skills": ["embedded systems", "debugging"],
    },
    "CE220": {
        "title": "Microprocessors",
        "credits": 3,
        "prereqs": ["CE120"],
        "skills": ["hardware", "assembly"],
    },
    "CE320": {
        "title": "Computer Networks",
        "credits": 3,
        "prereqs": ["CE210"],
        "skills": ["network protocols", "systems integration"],
    },
    "CE410": {
        "title": "Hardware/Software Co-Design",
        "credits": 3,
        "prereqs": ["CE210", "CE220"],
        "skills": ["systems design", "integration"],
    },
    "DS101": {
        "title": "Statistics I",
        "credits": 3,
        "prereqs": [],
        "skills": ["statistics", "statistical analysis"],
    },
    "DS120": {
        "title": "Python for Data",
        "credits": 3,
        "prereqs": [],
        "skills": ["python", "pandas"],
    },
    "DS220": {
        "title": "Data Wrangling",
        "credits": 3,
        "prereqs": ["DS120"],
        "skills": ["sql", "etl", "data cleaning"],
    },
    "DS230": {
        "title": "Data Visualization",
        "credits": 3,
        "prereqs": ["DS120"],
        "skills": ["tableau", "data visualization"],
    },
    "DS320": {
        "title": "Machine Learning",
        "credits": 3,
        "prereqs": ["DS220", "DS101"],
        "skills": ["machine learning", "predictive modeling"],
    },
    "DS410": {
        "title": "Data Science Capstone",
        "credits": 3,
        "prereqs": ["DS320", "DS230"],
        "skills": ["data storytelling", "project delivery"],
    },
    "BA101": {
        "title": "Business Foundations",
        "credits": 3,
        "prereqs": [],
        "skills": ["communication", "business analysis"],
    },
    "BA120": {
        "title": "Accounting Basics",
        "credits": 3,
        "prereqs": [],
        "skills": ["accounting", "financial literacy"],
    },
    "BA220": {
        "title": "Operations Management",
        "credits": 3,
        "prereqs": ["BA101"],
        "skills": ["operations management", "process improvement"],
    },
    "BA230": {
        "title": "Business Analytics",
        "credits": 3,
        "prereqs": ["BA101"],
        "skills": ["excel", "business analytics"],
    },
    "BA320": {
        "title": "Strategic Management",
        "credits": 3,
        "prereqs": ["BA220", "BA230"],
        "skills": ["strategy", "leadership"],
    },
    "BA410": {
        "title": "Business Capstone",
        "credits": 3,
        "prereqs": ["BA320"],
        "skills": ["project delivery", "leadership"],
    },
    "MKT101": {
        "title": "Marketing Principles",
        "credits": 3,
        "prereqs": [],
        "skills": ["marketing", "customer research"],
    },
    "MKT220": {
        "title": "Digital Marketing",
        "credits": 3,
        "prereqs": ["MKT101"],
        "skills": ["digital marketing", "seo"],
    },
    "MKT230": {
        "title": "Consumer Behavior",
        "credits": 3,
        "prereqs": ["MKT101"],
        "skills": ["customer research", "segmentation"],
    },
    "MKT320": {
        "title": "Marketing Analytics",
        "credits": 3,
        "prereqs": ["MKT220"],
        "skills": ["marketing analytics", "ab testing"],
    },
    "MKT410": {
        "title": "Brand Strategy",
        "credits": 3,
        "prereqs": ["MKT230", "MKT320"],
        "skills": ["branding", "strategy"],
    },
    "PM101": {
        "title": "Product Fundamentals",
        "credits": 3,
        "prereqs": [],
        "skills": ["product management", "communication"],
    },
    "PM220": {
        "title": "User Research",
        "credits": 3,
        "prereqs": ["PM101"],
        "skills": ["user research", "customer research"],
    },
    "PM230": {
        "title": "Agile Product Delivery",
        "credits": 3,
        "prereqs": ["PM101"],
        "skills": ["agile", "roadmapping"],
    },
    "PM320": {
        "title": "Product Analytics",
        "credits": 3,
        "prereqs": ["PM220"],
        "skills": ["product analytics", "sql"],
    },
    "PM410": {
        "title": "Product Strategy",
        "credits": 3,
        "prereqs": ["PM230", "PM320"],
        "skills": ["strategy", "stakeholder management"],
    },
}


DEGREE_REQUIREMENTS = {
    "Computer Science": ["CS101", "CS120", "CS210", "CS220", "CS230", "CS310", "CS330", "CS340", "CS360", "CS490"],
    "Cybersecurity": ["CY101", "CY220", "CY230", "CY310", "CY320", "CY410", "IT120", "IT220"],
    "Information Technology": ["IT101", "IT120", "IT220", "IT230", "IT320", "IT410", "CY101", "CY220"],
    "Computer Engineering": ["CE101", "CE120", "CE210", "CE220", "CE320", "CE410", "CS210", "CS340"],
    "Data Science": ["DS101", "DS120", "DS220", "DS230", "DS320", "DS410", "CS210", "CS230"],
    "Business Administration": ["BA101", "BA120", "BA220", "BA230", "BA320", "BA410", "MKT101", "PM101"],
    "Marketing": ["MKT101", "MKT220", "MKT230", "MKT320", "MKT410", "BA101", "BA230"],
    "Product Management": ["PM101", "PM220", "PM230", "PM320", "PM410", "BA101", "MKT101"],
}


INSTITUTION_STYLES = {
    "pathpilot_demo": {
        "label": "PathPilot Demo University",
        "prefix_map": {
            "CS": "CS",
            "CY": "CY",
            "IT": "IT",
            "CE": "CE",
            "DS": "DS",
            "BA": "BA",
            "MKT": "MKT",
            "PM": "PM",
        },
        "separator": "",
    },
    "northeast_state": {
        "label": "Northeast State College",
        "prefix_map": {
            "CS": "CSC",
            "CY": "CYS",
            "IT": "ITS",
            "CE": "ECE",
            "DS": "DAT",
            "BA": "BUS",
            "MKT": "MKT",
            "PM": "PRD",
        },
        "separator": "-",
    },
    "pacific_tech": {
        "label": "Pacific Tech Institute",
        "prefix_map": {
            "CS": "CIS",
            "CY": "SEC",
            "IT": "INF",
            "CE": "CMP",
            "DS": "DSC",
            "BA": "MGT",
            "MKT": "MKG",
            "PM": "PDM",
        },
        "separator": "",
    },
}


SKILL_TO_TITLES = {
    "python": ["Python Developer", "Data Analyst"],
    "machine learning": ["Machine Learning Engineer", "Data Scientist"],
    "predictive modeling": ["Machine Learning Engineer", "Data Scientist"],
    "sql": ["Data Analyst", "Database Administrator"],
    "data visualization": ["Data Analyst", "Business Intelligence Analyst"],
    "statistical analysis": ["Data Analyst", "Data Scientist"],
    "data storytelling": ["Data Analyst", "Business Analyst"],
    "cloud": ["Cloud Engineer", "Cloud Administrator"],
    "cloud security": ["Cloud Security Engineer", "Security Engineer"],
    "security": ["Security Analyst", "Cybersecurity Analyst"],
    "cybersecurity": ["Cybersecurity Analyst", "Security Engineer"],
    "network security": ["Security Analyst", "Network Security Engineer"],
    "penetration testing": ["Penetration Tester", "Security Engineer"],
    "digital forensics": ["Digital Forensics Analyst", "Incident Response Analyst"],
    "incident response": ["Incident Response Analyst", "Security Operations Analyst"],
    "siem": ["Security Operations Analyst", "Threat Detection Engineer"],
    "firewalls": ["Network Security Engineer", "Security Engineer"],
    "ci/cd": ["DevOps Engineer", "Site Reliability Engineer"],
    "systems administration": ["Systems Administrator", "IT Specialist"],
    "operating systems": ["Systems Engineer", "Site Reliability Engineer"],
    "networking": ["Network Engineer", "Systems Administrator"],
    "linux": ["Systems Engineer", "Site Reliability Engineer"],
    "software testing": ["QA Engineer", "Software Engineer"],
    "computer architecture": ["Embedded Software Engineer", "Systems Engineer"],
    "embedded systems": ["Embedded Software Engineer", "Firmware Engineer"],
    "hardware design": ["Hardware Engineer", "Embedded Engineer"],
    "network protocols": ["Network Engineer", "Systems Engineer"],
    "it service management": ["IT Service Manager", "Operations Manager"],
    "operations management": ["Operations Manager", "Business Operations Analyst"],
    "business analytics": ["Business Analyst", "Data Analyst"],
    "business analysis": ["Business Analyst", "Product Analyst"],
    "agile": ["Product Owner", "Product Manager"],
    "marketing": ["Marketing Specialist", "Marketing Manager"],
    "digital marketing": ["Digital Marketing Specialist", "Growth Marketing Manager"],
    "marketing analytics": ["Marketing Analyst", "Growth Analyst"],
    "customer research": ["UX Researcher", "Product Manager"],
    "product management": ["Product Manager", "Product Owner"],
    "user research": ["UX Researcher", "Product Manager"],
    "product analytics": ["Product Analyst", "Data Analyst"],
    "strategy": ["Strategy Analyst", "Product Manager"],
    "stakeholder management": ["Product Manager", "Program Manager"],
    "analytics": ["Business Analyst", "Product Analyst"],
}


def split_code(code):
    prefix = "".join(char for char in code if char.isalpha())
    number = "".join(char for char in code if char.isdigit())
    return prefix, number


def build_local_code(canonical_code, style):
    prefix, number = split_code(canonical_code)
    mapped_prefix = style["prefix_map"].get(prefix, prefix)
    separator = style["separator"]
    if separator:
        return f"{mapped_prefix}{separator}{number}"
    return f"{mapped_prefix}{number}"


def initialize_institution_maps():
    alias_to_canonical = {}
    canonical_to_local = {}
    for institution_key, style in INSTITUTION_STYLES.items():
        institution_alias_map = {}
        institution_local_map = {}
        for canonical_code in COURSE_CATALOG:
            local_code = build_local_code(canonical_code, style)
            institution_local_map[canonical_code] = local_code
            variants = {
                canonical_code,
                local_code,
                local_code.replace("-", ""),
                local_code.replace("-", " "),
            }
            for variant in variants:
                if variant:
                    institution_alias_map[variant.upper()] = canonical_code
        alias_to_canonical[institution_key] = institution_alias_map
        canonical_to_local[institution_key] = institution_local_map
    return alias_to_canonical, canonical_to_local


INSTITUTION_ALIAS_TO_CANONICAL, INSTITUTION_CANONICAL_TO_LOCAL = initialize_institution_maps()


def get_supported_institutions():
    return [
        {"key": key, "label": style["label"]}
        for key, style in INSTITUTION_STYLES.items()
    ]


def get_supported_degrees():
    return sorted(DEGREE_REQUIREMENTS.keys())


def normalize_institution(institution_key):
    if institution_key in INSTITUTION_STYLES:
        return institution_key
    return "pathpilot_demo"


def normalize_course_codes(raw_courses):
    if not raw_courses:
        return []
    cleaned = []
    for course in raw_courses:
        if not course:
            continue
        code = str(course).strip().upper()
        if code:
            cleaned.append(code)
    return sorted(set(cleaned))


def parse_courses_from_query(raw_courses):
    if not raw_courses:
        return []
    parsed = []
    for chunk in raw_courses:
        parsed.extend(part.strip() for part in str(chunk).split(","))
    return normalize_course_codes(parsed)


def map_course_codes_to_canonical(raw_courses, institution_key):
    institution = normalize_institution(institution_key)
    alias_map = INSTITUTION_ALIAS_TO_CANONICAL[institution]
    normalized = normalize_course_codes(raw_courses)
    mapped_codes = []
    unknown_codes = []
    canonical_codes = []

    for code in normalized:
        canonical = alias_map.get(code)
        if canonical:
            canonical_codes.append(canonical)
            mapped_codes.append(
                {
                    "input_code": code,
                    "canonical_code": canonical,
                    "recognized": True,
                }
            )
        else:
            unknown_codes.append(code)
            mapped_codes.append(
                {
                    "input_code": code,
                    "canonical_code": None,
                    "recognized": False,
                }
            )
    return sorted(set(canonical_codes)), mapped_codes, unknown_codes


def get_course_options(institution_key, degree):
    institution = normalize_institution(institution_key)
    local_map = INSTITUTION_CANONICAL_TO_LOCAL[institution]
    required_codes = DEGREE_REQUIREMENTS.get(degree, [])
    options = []
    for canonical_code in required_codes:
        course = COURSE_CATALOG[canonical_code]
        local_code = local_map.get(canonical_code, canonical_code)
        options.append(
            {
                "value": local_code,
                "canonical_code": canonical_code,
                "label": f"{local_code} - {course['title']}",
                "title": course["title"],
                "credits": course["credits"],
            }
        )
    return options


def build_degree_plan(
    degree,
    completed_courses=None,
    transfer_credits=0,
    max_credits_per_term=12,
    institution_key="pathpilot_demo",
):
    institution = normalize_institution(institution_key)
    required_codes = DEGREE_REQUIREMENTS.get(degree, [])
    canonical_completed, input_mapping, unknown_codes = map_course_codes_to_canonical(
        completed_courses,
        institution,
    )
    completed_codes = list(canonical_completed)
    completed_codes_set = set(completed_codes)
    completed_required = sorted(code for code in required_codes if code in completed_codes_set)
    pending = set(code for code in required_codes if code not in completed_codes_set)
    pending_before_planning = set(pending)
    term_num = 1
    plan_terms = []
    completed_dynamic = set(completed_required)

    while pending and term_num <= 12:
        eligible = []
        for code in sorted(pending):
            prereqs = COURSE_CATALOG[code]["prereqs"]
            if all(pr in completed_dynamic for pr in prereqs):
                eligible.append(code)

        term_courses = []
        used = 0
        for code in eligible:
            credits = COURSE_CATALOG[code]["credits"]
            if used + credits <= max_credits_per_term:
                term_courses.append(code)
                used += credits

        if not term_courses:
            break

        plan_terms.append(
            {
                "term": f"Term {term_num}",
                "credits": used,
                "courses": [serialize_course(code, institution) for code in term_courses],
            }
        )
        completed_dynamic.update(term_courses)
        pending.difference_update(term_courses)
        term_num += 1

    blocked = [serialize_course(code, institution) for code in sorted(pending)]
    required_credit_total = sum(COURSE_CATALOG[code]["credits"] for code in required_codes)
    completed_known_credits = sum(COURSE_CATALOG[code]["credits"] for code in completed_required)
    completed_total_credits = max(0, int(transfer_credits)) + completed_known_credits
    remaining_required_credits = sum(COURSE_CATALOG[code]["credits"] for code in pending_before_planning)
    planned_required_credits = sum(term["credits"] for term in plan_terms)
    unplanned_required_credits = sum(COURSE_CATALOG[code]["credits"] for code in pending)
    estimated_total_remaining = max(0, PROGRAM_TOTAL_CREDITS - completed_total_credits)

    # Skill personalization should reflect only completed/selected courses,
    # not future roadmap courses.
    skills = build_skill_profile(completed_codes)
    matching_skill_keywords = build_matching_skill_keywords(completed_codes)
    recommended_titles = recommend_titles_from_skills(skills)

    notes = []
    if blocked:
        notes.append("Some courses are blocked by missing prerequisites; complete prior terms first.")
    if unknown_codes:
        notes.append("Some entered course codes were not recognized for the selected institution.")

    return {
        "degree": degree,
        "institution_key": institution,
        "institution_label": INSTITUTION_STYLES[institution]["label"],
        "required_course_count": len(required_codes),
        "completed_courses": [serialize_course(code, institution) for code in completed_required],
        "remaining_courses": [serialize_course(code, institution) for code in sorted(pending)],
        "semester_plan": plan_terms,
        "blocked_courses": blocked,
        "max_credits_per_term": max_credits_per_term,
        "required_credits_total": required_credit_total,
        "completed_credits_estimate": completed_total_credits,
        "remaining_required_credits": remaining_required_credits,
        "planned_required_credits": planned_required_credits,
        "unplanned_required_credits": unplanned_required_credits,
        "estimated_total_remaining_credits": estimated_total_remaining,
        "skill_profile": skills,
        "matching_skill_keywords": matching_skill_keywords,
        "recommended_private_titles": recommended_titles,
        "course_input_mapping": input_mapping,
        "unrecognized_course_codes": unknown_codes,
        "notes": notes,
    }


def serialize_course(code, institution_key="pathpilot_demo"):
    institution = normalize_institution(institution_key)
    course = COURSE_CATALOG[code]
    local_map = INSTITUTION_CANONICAL_TO_LOCAL[institution]
    local_code = local_map.get(code, code)
    return {
        "code": local_code,
        "canonical_code": code,
        "title": course["title"],
        "credits": course["credits"],
        "prereqs": [local_map.get(prereq, prereq) for prereq in course["prereqs"]],
        "prereqs_canonical": course["prereqs"],
        "skills": course["skills"],
    }


def build_skill_profile(completed_codes):
    counter = count_skills(completed_codes)
    return [{"skill": skill, "weight": weight} for skill, weight in counter.most_common(8)]


def build_matching_skill_keywords(completed_codes):
    counter = count_skills(completed_codes)
    return [skill for skill, _weight in counter.most_common()]


def count_skills(completed_codes):
    counter = Counter()
    for code in completed_codes:
        if code not in COURSE_CATALOG:
            continue
        for skill in COURSE_CATALOG[code]["skills"]:
            counter[skill] += 1
    return counter


def recommend_titles_from_skills(skill_profile):
    titles = []
    for entry in skill_profile:
        skill = entry["skill"]
        for role in SKILL_TO_TITLES.get(skill, []):
            if role not in titles:
                titles.append(role)
    return titles[:10]
