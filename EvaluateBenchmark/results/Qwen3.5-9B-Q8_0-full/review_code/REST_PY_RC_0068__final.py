import requests

def solve(inputs):
    """
    Look up countries by exact match on their three-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Three-letter ISO country code to match exactly
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of attributes to exclude from response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    # Extract inputs
    iso_code = inputs["value"]
    skip = inputs["results_to_skip"]
    exclude_attrs = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build the API URL for REST Countries v5
    # Using the /v3.1/countries/{code} endpoint for exact match by ISO code
    base_url = "https://api.restcountries.com/v3.1"
    url = f"{base_url}/countries/{iso_code}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Check for unsuccessful HTTP response
        if not response.ok:
            raise Exception(f"HTTP error: {response.status_code} - {response.text}")
        
        # Decode JSON response
        data = response.json()
        
        # Handle empty response
        if data is None or (isinstance(data, dict) and len(data) == 0):
            return None
        
        # Filter out excluded attributes if any
        if exclude_attrs:
            filtered_data = {}
            for key, value in data.items():
                if key not in exclude_attrs:
                    filtered_data[key] = value
            return filtered_data
        
        return data
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")