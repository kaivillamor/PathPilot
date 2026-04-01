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
        usajobs_response.raise_for_status()
        usajobs_filtered_data =  usajobs_response.json()
        usajobs = usajobs_filtered_data["SearchResult"]["SearchResultItems"]
        filtered_usajobs = []
        for job in usajobs:
            descriptor = job["MatchedObjectDescriptor"]
            remuneration = descriptor.get("PositionRemuneration")
            remote = descriptor.get("UserArea")
            # Note the descriptor was ApplyURI instead of ApplyURL 
            url = descriptor.get("ApplyURI")
            filtered_usajobs.append({
                # filtered to just title for now
                # note: use get to avoid null breaking the app
                "title": descriptor.get("PositionTitle"),
                "Organization": descriptor.get("OrganizationName"),
                "location": descriptor.get("PositionLocationDisplay"),
                "salary_min": remuneration[0]["MinimumRange"] if remuneration else None,
                "salary_max": remuneration[0]["MaximumRange"] if remuneration else None,
                "Remote": remote.get("Details", {}).get("RemoteIndicator") if remote else None,
                "ApplicationClose": descriptor.get("ApplicationCloseDate"),
                "URL": url[0] if url else None
            })
        return filtered_usajobs
    except Exception as e:
        return {"error": f"USAJobs API failed: {str(e)}"}