import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip.
            - included_fields (str): Fields to return, separated by commas.
    
    Returns:
        dict or None: Decoded JSON response, or None for a successful empty response.
    
    Raises:
        Exception: For an unsuccessful HTTP response.
    """
    base_url = "https://dummyjson.com/posts"
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 1,
        "_fields": inputs["included_fields"]
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        if response.status_code == 204:
            return None
        
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")