import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Currency code to match exactly
            - results_to_skip (int): Number of results to skip
            - included_attributes (list): Attributes to return for each country
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
        Raises: Exception for unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5.0"
    endpoint = "/currencies"
    
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Authorization": inputs["credential"]
    }
    
    params = {
        "code": inputs["value"],
        "skip": inputs["results_to_skip"]
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter to only included attributes
    if inputs["included_attributes"]:
        filtered_data = []
        for country in data.get("countries", []):
            filtered_country = {}
            for attr in inputs["included_attributes"]:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data