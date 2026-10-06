import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON with pagination and sorting.
    
    Args:
        inputs (dict): Must contain 'results_to_skip' and 'sort_field'.
        
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/users"
    
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 1,
        "sort_by": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    
    data = response.json()
    
    # DummyJSON returns a dict with 'users' key, not an array directly.
    # The task says "Return None for a successful empty response."
    # If the users list is empty, return None.
    if not data.get("users"):
        return None
    
    return data