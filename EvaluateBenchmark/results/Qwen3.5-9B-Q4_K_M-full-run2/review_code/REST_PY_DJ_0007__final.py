import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON and return the decoded JSON response.
    
    Args:
        inputs (dict): Must contain 'page' key with an integer value for pagination.
        
    Returns:
        dict or None: The decoded JSON response, or None if the response is empty.
        
    Raises:
        requests.exceptions.HTTPError: If the HTTP response status code indicates failure.
    """
    base_url = "https://dummyjson.com/users"
    
    page = inputs.get("page", 1)
    params = {"page": page}
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data