import requests

def solve(inputs):
    """
    Look up countries by exact match on calling code from REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: The calling code to match exactly
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    base_url = "https://api.restcountries.com"
    endpoint = f"/v5/calling-code/{value}"
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # If the response is empty (no countries found), return None
    if not data:
        return None
    
    # Filter attributes if specified
    if included_attributes:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for attr in included_attributes:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data