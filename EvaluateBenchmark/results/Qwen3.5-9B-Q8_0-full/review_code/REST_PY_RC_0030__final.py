import requests

def solve(inputs):
    """
    Search country names using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return
            - excluded_attributes (list): List of attributes to exclude from results
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied API key/credential
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com/v5"
    search_text = inputs["search_text"]
    result_limit = inputs["result_limit"]
    excluded_attributes = inputs["excluded_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "name": search_text,
        "limit": str(result_limit)
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    try:
        response = requests.get(
            f"{base_url}/countries",
            params=params,
            headers=headers
        )
        
        if response.status_code != 200:
            raise Exception(f"HTTP error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        # If the response is empty (successful but no results), return None
        if not data:
            return None
        
        # Filter out excluded attributes from each country object
        if excluded_attributes:
            filtered_data = []
            for country in data:
                filtered_country = {k: v for k, v in country.items() 
                                  if k not in excluded_attributes}
                filtered_data.append(filtered_country)
            return filtered_data
        
        return data
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")