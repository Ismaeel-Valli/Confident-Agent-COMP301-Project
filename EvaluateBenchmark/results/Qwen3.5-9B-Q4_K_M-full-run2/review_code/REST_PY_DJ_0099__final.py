import requests

def solve(inputs):
    result_limit = inputs["result_limit"]
    included_fields = inputs["included_fields"]
    
    base_url = "https://dummyjson.com/posts"
    params = {
        "limit": result_limit,
        "fields": included_fields
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    return response.json()