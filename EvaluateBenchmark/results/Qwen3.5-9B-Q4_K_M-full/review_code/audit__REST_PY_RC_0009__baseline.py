import requests

def solve(inputs):
    """
    Retrieves one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'results_to_skip' (int): Number of results to skip (offset).
            - 'credential' (str): Caller-supplied credential (e.g., API key or token).
    
    Returns:
        dict or None: The decoded JSON response. Returns None for a successful empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx range).
    """
    base_url = "https://restcountries.com/v5"
    endpoint = "/geonames"  # Example endpoint; adjust if specific country list endpoint is needed
    
    # Construct query parameters
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 100  # Typical page size; can be adjusted based on requirements
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}" if inputs['credential'].startswith("Bearer ") else inputs['credential']
    }
    
    url = f"{base_url}{endpoint}"
    
    try:
        response = requests.get(url, params=params, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (non-2xx status codes)
        response.raise_for_status()
        
        data = response.json()
        
        # Return None if the response is successfully empty
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Unsuccessful HTTP response: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")