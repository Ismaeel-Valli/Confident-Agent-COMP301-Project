import requests

def solve(inputs):
    """
    Look up countries by an exact match on their bordering country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The country code to match exactly against borders
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    """
    value = inputs["value"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    url = f"https://api.restcountries.com/v5.0/countries/border/{value}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If the response is an empty list or object indicating no results, return None
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