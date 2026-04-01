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
                "title": descriptor["PositionTitle"],
                "Organization": descriptor["OrganizationName"],
                "location": descriptor["PositionLocationDisplay"],
                "salary_min": descriptor["PositionRemuneration"][0]["MinimumRange"],
                "salary_max": descriptor["PositionRemuneration"][0]["MaximumRange"],       
                "Remote": descriptor["UserArea"]["Details"]["RemoteIndicator"],
                "ApplicationClose": descriptor["ApplicationCloseDate"],
                # Note the descriptor was ApplyURI instead of ApplyURL 
                "URL": descriptor["ApplyURI"][0]
            })
        return filtered_usajobs
    except Exception as e:
        return {"error": f"USAJobs API failed: {str(e)}"}