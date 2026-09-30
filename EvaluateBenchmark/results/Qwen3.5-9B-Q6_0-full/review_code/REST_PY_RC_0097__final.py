import requests

def solve(inputs):
    """
    Look up countries by exact match on their subregion using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The subregion to match exactly
            - results_to_skip: Number of results to skip (pagination)
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    subregion = inputs["value"]
    skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5.1/subregions/{subregion}"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Skip the requested number of results
    if isinstance(data, list):
        skipped_data = data[skip:]
        return skipped_data if skipped_data else None
    
    return data