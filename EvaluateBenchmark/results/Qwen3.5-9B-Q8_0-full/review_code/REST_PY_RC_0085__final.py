import requests

def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The region to match exactly
            - results_to_skip: Number of results to skip (for pagination)
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    region = inputs["value"]
    skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # Build the request URL with query parameters
    params = {
        "region": region,
        "skip": skip
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (empty list)
    if not data:
        return None
    
    return data