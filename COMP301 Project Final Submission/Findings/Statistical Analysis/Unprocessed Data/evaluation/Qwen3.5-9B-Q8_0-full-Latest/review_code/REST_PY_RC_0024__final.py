import requests

def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): Two-letter ISO country code to match exactly
            - result_limit (int): Maximum number of results to return
            - results_to_skip (int): Number of results to skip
            - credential (str): Caller-supplied API key/credential
    
    Returns:
        list or None: Decoded JSON response as a list, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    iso_code = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # Build the query parameters for exact match on ISO code
    params = {
        "iso2": iso_code,
        "limit": result_limit,
        "skip": results_to_skip
    }
    
    url = f"{base_url}/restcountries"
    
    try:
        response = requests.get(url, params=params, headers={"Authorization": f"Bearer {credential}"})
        
        if response.status_code == 200:
            data = response.json()
            # Return None for successful empty response (no countries found)
            return data if data else None
        else:
            raise Exception(f"HTTP error: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")