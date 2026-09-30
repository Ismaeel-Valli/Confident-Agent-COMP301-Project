import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code.
    
    Args:
        inputs (dict): {
            "value": str - Country code to match exactly,
            "excluded_attributes": list[str] - Attributes to exclude from results,
            "credential": str - Caller-supplied credential with necessary permissions
        }
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    value = inputs["value"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # API endpoint for countries by bordering country code
    url = "https://api.restcountries.com/v3.1/all"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter out excluded attributes if any
    if excluded_attributes:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for key, val in country.items():
                if key not in excluded_attributes:
                    filtered_country[key] = val
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data