import requests

def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The region to match exactly
            - excluded_attributes: List of country attributes to exclude from results
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    region = inputs["value"]
    credential = inputs["credential"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    
    # Build the request URL with region parameter
    url = f"{base_url}/v5.0/countries?region={region}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an exception for unsuccessful HTTP responses
        
        data = response.json()
        
        # If the response is empty (successful but no countries found), return None
        if not data:
            return None
        
        # Filter out excluded attributes from each country object
        filtered_countries = []
        for country in data:
            filtered_country = {}
            for key, value in country.items():
                if key not in excluded_attributes:
                    filtered_country[key] = value
            filtered_countries.append(filtered_country)
        
        return filtered_countries
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")