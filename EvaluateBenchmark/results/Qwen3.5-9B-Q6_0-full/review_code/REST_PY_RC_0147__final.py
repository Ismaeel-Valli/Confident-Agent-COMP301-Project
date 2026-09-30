import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5.
    
    Args:
        inputs (dict): Must contain:
            - 'value': The capital city to match exactly
            - 'excluded_attributes': List of country attributes to exclude from results
            - 'credential': Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    value = inputs["value"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # REST Countries v5 endpoint for searching by capital
    base_url = "https://api.restcountries.com/v5"
    url = f"{base_url}/search/capital/{value}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter out countries with excluded attributes
    if excluded_attributes:
        filtered_data = []
        for country in data:
            include = True
            for attr in excluded_attributes:
                if attr in country and country[attr]:
                    include = False
                    break
            if include:
                filtered_data.append(country)
        return filtered_data
    
    return data