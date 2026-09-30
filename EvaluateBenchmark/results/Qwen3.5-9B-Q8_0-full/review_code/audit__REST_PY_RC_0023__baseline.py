import requests

def solve(inputs):
    """
    Searches for countries using the REST Countries v5 API based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip (for pagination).
            - search_text (str): The search term for country names or codes.
            - credential (str): API key/credential for authentication.
    
    Returns:
        list or None: A list of decoded JSON objects representing the search results, 
                      or None if the response is successfully empty.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://restcountries.com/v5.1/search"
    
    params = {
        "search": inputs["search_text"],
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code: {response.status_code}")
    
    data = response.json()
    
    # If the response is an empty list (successful but no results), return None as per instructions
    if not data:
        return None
    
    return data