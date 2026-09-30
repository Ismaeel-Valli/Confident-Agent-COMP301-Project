import requests

def solve(inputs):
    """
    Searches country codes using REST Countries v5 API based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip.
            - search_text (str): Search term for country codes.
            - credential (str): Caller-supplied credential (e.g., API key).
    
    Returns:
        dict or None: Decoded JSON response if successful; None for an empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://restcountries.com/v5.1/data"
    params = {
        "result_limit": inputs["result_limit"],
        "results_to_skip": inputs["results_to_skip"],
        "search_text": inputs["search_text"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code: {response.status_code}")
    
    data = response.json()
    
    # REST Countries v5 returns a list of country objects. 
    # If the search yields no results, the list will be empty.
    if not data:
        return None
    
    return data