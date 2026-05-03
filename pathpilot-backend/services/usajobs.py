import requests
import os


def extract_label_list(value):
    if not value:
        return []
    if isinstance(value, list):
        labels = []
        for item in value:
            if isinstance(item, dict):
                label = item.get("Name") or item.get("Code")
                if label:
                    labels.append(str(label))
            elif item:
                labels.append(str(item))
        return labels
    if isinstance(value, dict):
        label = value.get("Name") or value.get("Code")
        return [str(label)] if label else []
    return [str(value)]


def get_usajobs(usajobs_series):
    # usajobs api call
    try:
        usajobs_response = requests.get(
            "https://data.usajobs.gov/api/search",
            headers={
                "User-Agent": os.getenv("USAJOBS_EMAIL"),
                "Authorization-Key": os.getenv("USAJOBS_API_KEY"),
            },
            params={
                "JobCategoryCode": usajobs_series,
                "ResultsPerPage": 10,
            },
            timeout=10,
        )
        usajobs_response.raise_for_status()
        usajobs_filtered_data = usajobs_response.json()
        usajobs = usajobs_filtered_data["SearchResult"]["SearchResultItems"]
        filtered_usajobs = []
        for job in usajobs:
            descriptor = job["MatchedObjectDescriptor"]
            remuneration = descriptor.get("PositionRemuneration")
            remote = descriptor.get("UserArea")
            user_details = remote.get("Details", {}) if remote else {}
            # Note the descriptor was ApplyURI instead of ApplyURL
            url = descriptor.get("ApplyURI")
            filtered_usajobs.append({
                # note: use get to avoid null breaking the app
                "title": descriptor.get("PositionTitle"),
                "organization": descriptor.get("OrganizationName"),
                "location": descriptor.get("PositionLocationDisplay"),
                "salary_min": remuneration[0]["MinimumRange"] if remuneration else None,
                "salary_max": remuneration[0]["MaximumRange"] if remuneration else None,
                "salary_interval": remuneration[0].get("RateIntervalCode") if remuneration else None,
                "remote": user_details.get("RemoteIndicator"),
                "applicationclose": descriptor.get("ApplicationCloseDate"),
                "applicationopen": descriptor.get("PublicationStartDate"),
                "job_summary": user_details.get("JobSummary"),
                "qualification_summary": descriptor.get("QualificationSummary"),
                "requirements": user_details.get("MajorDuties"),
                "security_clearance": descriptor.get("SecurityClearance"),
                "position_schedule": ", ".join(extract_label_list(descriptor.get("PositionSchedule"))),
                "position_offering_type": descriptor.get("PositionOfferingType"),
                "url": url[0] if url else None
            })
        return filtered_usajobs
    except Exception as e:
        return {"error": f"USAJobs API failed: {str(e)}"}
