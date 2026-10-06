import requests

def solve(inputs):
    """
    Searches for countries using the REST Countries v5 API based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip (for pagination).
            - search_text (str): The search term for country names.
            - credential (str): API key or token with necessary permissions.
    
    Returns:
        list or None: Decoded JSON response as a list of countries, or None if the response is empty but successful.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://restcountries.com/v3.1"
    endpoint = f"{base_url}/search"
    
    params = {
        "name": inputs["search_text"],
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(endpoint, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If the response is an empty list, return None as per instructions
    if not data:
        return None
    
    return data