import requests

def solve(inputs):
    """
    Look up countries by exact match on their calling code from REST Countries v5.
    
    Args:
        inputs (dict): {
            "value": str - The calling code to match exactly,
            "excluded_attributes": list[str] - Attributes to exclude from results,
            "credential": str - Caller-supplied credential with necessary permissions
        }
    
    Returns:
        dict or None: Decoded JSON response. None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    calling_code = inputs["value"]
    credential = inputs["credential"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    
    # Build query parameters
    params = {
        "callingcode": calling_code,
        "crd": credential  # Assuming 'crd' is the credential parameter name for REST Countries v5
    }
    
    response = requests.get(f"{base_url}/v3.1/all", params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Filter out excluded attributes if any
    if excluded_attributes:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for key, value in country.items():
                if key not in excluded_attributes:
                    filtered_country[key] = value
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data