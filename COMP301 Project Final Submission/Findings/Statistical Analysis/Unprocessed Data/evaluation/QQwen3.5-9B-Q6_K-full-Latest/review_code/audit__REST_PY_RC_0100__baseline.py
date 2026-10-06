import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their subregion using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The subregion value to match exactly.
            - 'result_limit': Maximum number of results to return.
            - 'results_to_skip': Number of results to skip (offset).
            - 'credential': Caller-supplied credential (e.g., API key or token).
    
    Returns:
        list or None: The decoded JSON response as a list of country objects, 
                      or None if the response is successfully empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx range).
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]

    # Construct the API URL for REST Countries v5 with subregion filter
    base_url = "https://restcountries.com/v3.1/subregion"
    params = {
        "name": value,
        "limit": result_limit,
        "skip": results_to_skip
    }

    headers = {
        "Authorization": f"Bearer {credential}" if credential.startswith("Bearer ") else f"{credential}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (non-2xx status codes)
        response.raise_for_status()
        
        data = response.json()
        
        # Return None for a successful empty response
        if not data:
            return None
        
        return data

    except requests.exceptions.HTTPError as e:
        raise Exception(f"Unsuccessful HTTP response: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")