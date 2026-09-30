import requests


def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Must contain:
            - "value": Currency code to match exactly
            - "excluded_attributes": List of country attributes to exclude from results
            - "credential": Caller-supplied credential with necessary permissions
    
    Returns:
        list or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    value = inputs["value"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    base_url = "https://api.restcountries.com/v5"
    url = f"{base_url}/currency/{value}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    if isinstance(data, list):
        if len(data) == 0:
            return None
        
        filtered_data = []
        for country in data:
            filtered_country = {}
            for key, val in country.items():
                if key not in excluded_attributes:
                    filtered_country[key] = val
            filtered_data.append(filtered_country)
        
        return filtered_data
    
    elif isinstance(data, dict):
        filtered_data = {}
        for key, val in data.items():
            if key not in excluded_attributes:
                filtered_data[key] = val
        return filtered_data
    
    else:
        return data