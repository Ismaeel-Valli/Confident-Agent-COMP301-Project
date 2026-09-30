import requests

def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: The two-letter ISO country code to match exactly
            - results_to_skip: Number of results to skip
            - included_attributes: List of attributes to include in the response
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    country_code = inputs["value"]
    skip = inputs["results_to_skip"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Construct the API endpoint for exact match lookup
    url = f"{base_url}/v5.1/country/{country_code}"
    
    # Prepare headers with the credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Check for unsuccessful HTTP responses
        if not response.ok:
            raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
        
        # Decode the JSON response
        data = response.json()
        
        # If no results found (empty response), return None
        if not data or (isinstance(data, list) and len(data) == 0):
            return None
        
        # Filter to only include requested attributes
        if isinstance(data, list):
            filtered_results = []
            for country in data:
                filtered_country = {}
                for attr in attributes:
                    if attr in country:
                        filtered_country[attr] = country[attr]
                filtered_results.append(filtered_country)
            return filtered_results
        else:
            # Single object response
            filtered_country = {}
            for attr in attributes:
                if attr in data:
                    filtered_country[attr] = data[attr]
            return filtered_country
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")