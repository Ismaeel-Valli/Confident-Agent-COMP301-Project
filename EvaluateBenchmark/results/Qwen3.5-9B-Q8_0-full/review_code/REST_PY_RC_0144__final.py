import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The capital city to match exactly
            - result_limit: Maximum number of results to return
            - credential: Caller-supplied credential for authentication
    
    Returns:
        list or None: Decoded JSON response as a list, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    capital = inputs["value"]
    limit = inputs["result_limit"]
    credential = inputs["credential"]
    
    # REST Countries v5 uses /v3/search/capital/{capital} endpoint
    url = f"{base_url}/v3/search/capital/{capital}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses
        
        data = response.json()
        
        # Apply result limit if specified
        if limit is not None and limit > 0:
            return data[:limit]
        elif limit == 0:
            return []
        else:
            return data
            
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except ValueError as e:
        raise Exception(f"Failed to decode JSON response: {e}")