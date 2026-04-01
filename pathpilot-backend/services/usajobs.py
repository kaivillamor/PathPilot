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
        usajobs_filtered_data =  usajobs_response.json()
        usajobs = usajobs_filtered_data["SearchResult"]["SearchResultItems"]
        filtered_usajobs = []
        for job in usajobs:
            descriptor = job["MatchedObjectDescriptor"]
            filtered_usajobs.append({
                # filtered to just title for now
                "title": descriptor["PositionTitle"]
            })
        return filtered_usajobs
    except Exception as e:
        return {"error": f"USAJobs API failed: {str(e)}"}