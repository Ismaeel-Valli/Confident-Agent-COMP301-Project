import requests

def solve(inputs):
    """
    Search country names using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - excluded_attributes (list): Attributes to exclude from results
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
    """
    base_url = "https://api.restcountries.com/v5"
    
    # Build query parameters
    params = {
        "search": inputs["search_text"],
        "credential": inputs["credential"]
    }
    
    # Make the request
    response = requests.get(base_url, params=params)
    
    # Raise exception for unsuccessful HTTP response
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Return None for successful empty response
    if len(data) == 0:
        return None
    
    # Filter out excluded attributes
    if inputs.get("excluded_attributes"):
        filtered_data = []
        for country in data:
            filtered_country = {}
            for key, value in country.items():
                if key not in inputs["excluded_attributes"]:
                    filtered_country[key] = value
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data