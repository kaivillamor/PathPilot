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
        return theirstack_response.json()
    except Exception as e:
        return {"error": f"TheirStack API failed: {str(e)}"}