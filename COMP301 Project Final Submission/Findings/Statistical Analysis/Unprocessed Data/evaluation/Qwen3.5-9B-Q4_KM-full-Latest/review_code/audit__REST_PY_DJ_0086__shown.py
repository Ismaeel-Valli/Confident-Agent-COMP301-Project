import requests

def solve(inputs):
    """Retrieve one page of users from DummyJSON with pagination."""
    base_url = "https://dummyjson.com/users"
    
    result_limit = inputs.get("result_limit", 10)
    results_to_skip = inputs.get("results_to_skip", 0)
    
    params = {
        "limit": result_limit,
        "skip": results_to_skip
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    return response.json()