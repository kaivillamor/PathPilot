import requests
import os

def get_usajobs(usajobs_series):
     # usajobs api call
    try:
        usajobs_response = requests.get(
            "https://data.usajobs.gov/api/search", 
            headers = {
                "User-Agent": os.getenv("USAJOBS_EMAIL"),
                "Authorization-Key": os.getenv("USAJOBS_API_KEY")
            },
            params={
                'JobCategoryCode': usajobs_series,
                "ResultsPerPage": 10
            },
            timeout = 10
        )
        return usajobs_response.json()
    except Exception as e:
        return {"error": f"USAJobs API failed: {str(e)}"}