import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON, skipping a number of results.
    
    Args:
        inputs (dict): Dictionary containing 'results_to_skip' key.
        
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/users"
    
    # Build query parameters
    params = {"skip": inputs["results_to_skip"]}
    
    try:
        response = requests.get(base_url, params=params)
        
        if response.status_code != 200:
            raise Exception(f"HTTP error {response.status_code}: {response.text}")
            
        data = response.json()
        
        # Return None for empty results, otherwise return the decoded JSON
        if not data.get("users"):
            return None
            
        return data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")