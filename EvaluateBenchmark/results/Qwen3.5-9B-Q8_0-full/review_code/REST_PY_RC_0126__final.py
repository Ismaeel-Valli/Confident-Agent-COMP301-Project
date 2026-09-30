import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - value: Currency code to match exactly
            - result_limit: Maximum number of results
            - excluded_attributes: List of country attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # REST Countries v5 API endpoint for filtering by currency code
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5.0/countries?currency={value}&limit={result_limit}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # If the response is an empty list (no countries found), return None
        if isinstance(data, list) and len(data) == 0:
            return None
        
        # Filter out excluded attributes from each country object
        if excluded_attributes:
            filtered_data = []
            for country in data:
                filtered_country = {key: value for key, value in country.items() 
                                   if key not in excluded_attributes}
                filtered_data.append(filtered_country)
            return filtered_data
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")