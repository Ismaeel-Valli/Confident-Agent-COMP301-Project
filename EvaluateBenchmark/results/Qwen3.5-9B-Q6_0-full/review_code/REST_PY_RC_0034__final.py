import requests

def solve(inputs):
    """
    Search country names on REST Countries v5 API.
    
    Args:
        inputs (dict): Must contain:
            - results_to_skip (int): Number of results to skip (offset)
            - included_attributes (list[str]): Attributes to include in response
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied API key
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/search/name"
    
    url = f"{base_url}{endpoint}"
    
    params = {
        "search": inputs["search_text"],
        "skip": inputs["results_to_skip"]
    }
    
    headers = {
        "X-Auth-Token": inputs["credential"],
        "Accept": "application/json"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter to only included attributes if specified
    if inputs["included_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for attr in inputs["included_attributes"]:
                if isinstance(country, dict) and attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data