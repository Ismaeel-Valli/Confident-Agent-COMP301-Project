import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON with pagination and sorting.
    
    Args:
        inputs (dict): Must contain 'results_to_skip' (int) and 'sort_field' (str).
        
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful (status code >= 400).
    """
    base_url = "https://dummyjson.com/users"
    
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 1,
        "sort_by": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code >= 400:
        raise Exception(f"HTTP error {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response (empty users array)
    if not data.get("users") or len(data["users"]) == 0:
        return None
    
    return data