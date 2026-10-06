import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their common country name using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The country name to match exactly.
            - 'results_to_skip': Number of results to skip (for pagination).
            - 'credential': Caller-supplied credential (API key or token).
    
    Returns:
        list or None: Decoded JSON response as a list of countries, or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code outside 200-299 range).
    """
    value = inputs["value"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # REST Countries v5 API endpoint for searching by common name
    base_url = "https://restcountries.com/v3.1/name"
    
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
        response = requests.get(base_url, params=params, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None for a successful empty response
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")