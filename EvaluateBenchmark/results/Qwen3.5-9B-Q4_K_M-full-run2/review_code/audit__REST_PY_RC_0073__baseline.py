import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their common country name using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The exact country name to search for.
            - 'results_to_skip': Number of results to skip (for pagination).
            - 'credential': Caller-supplied credential (e.g., API key or token).
    
    Returns:
        list or None: Decoded JSON response if results exist, None if the response is successfully empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code >= 400).
    """
    value = inputs["value"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]

    # Base URL for REST Countries v5 API
    base_url = "https://restcountries.com/v3.1"
    
    # Construct the query parameters
    params = {
        "name": value,
        "skip": results_to_skip
    }

    headers = {
        "Authorization": f"Bearer {credential}" if credential.startswith("Bearer ") else f"{credential}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(f"{base_url}/country", params=params, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None if the response is successfully empty
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Unsuccessful HTTP response: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")