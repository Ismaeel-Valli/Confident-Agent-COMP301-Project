import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Three-letter ISO country code to match exactly
            - result_limit: Maximum number of results to return
            - included_attributes: List of country attributes to include in response
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
        Raises: Exception for unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build the URL with the country code parameter
    url = f"{base_url}/v5.0/country/{inputs['value']}"
    
    # Make the request with the provided credential
    response = requests.get(url, headers={"Authorization": inputs["credential"]})
    
    # Check for unsuccessful HTTP response
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    # Decode the JSON response
    data = response.json()
    
    # If no countries found (empty list), return None as per spec
    if isinstance(data, list) and len(data) == 0:
        return None
    
    # Filter to only include requested attributes
    if inputs["included_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for attr in inputs["included_attributes"]:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        return filtered_data
    
    # Return the full response as-is
    return data