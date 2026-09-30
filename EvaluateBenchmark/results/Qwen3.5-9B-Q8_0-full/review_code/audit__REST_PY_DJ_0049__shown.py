import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON, skipping a specified number of results.
    
    Args:
        inputs (dict): Dictionary containing 'results_to_skip' (int).
        
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/users"
    
    # Build the query parameters
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 1  # Retrieve one page (one result)
    }
    
    try:
        response = requests.get(base_url, params=params)
        
        # Raise an exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None for successful empty response (empty users array)
        if not data.get("users"):
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")