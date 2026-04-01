import requests
import os

def get_theirstack(theirstack_title):
    # theirstack api call
    try:
        theirstack_response = requests.post(
            "https://api.theirstack.com/v1/jobs/search",
            headers = {
                "Authorization": f"Bearer {os.getenv('THEIRSTACK_API_KEY')}",
                'Content-Type': 'application/json'
            },
            json = {
                'job_title_or': theirstack_title,
                'job_country_code_or': ['US'],
                'posted_at_max_age_days': 30,
                'limit': 10,
                'page': 0
            },
            timeout = 10
        )
        theirstack_filtered_data = theirstack_response.json()
        filtered_theirstackjobs = []
        for job in theirstack_filtered_data["data"]:
            filtered_theirstackjobs.append({
                "title": job["job_title"],
                "company": job["company"],
                "location": job["location"],
                "remote": job["remote"],
                "salary_string": job["salary_string"],
                "salary_min": job["min_annual_salary_usd"],
                "salary_max": job["max_annual_salary_usd"],
                "url": job["url"],
                "date_posted": job["date_posted"],
                "seniority": job["seniority"]
            })
        return filtered_theirstackjobs
    except Exception as e:
        return {"error": f"TheirStack API failed: {str(e)}"}