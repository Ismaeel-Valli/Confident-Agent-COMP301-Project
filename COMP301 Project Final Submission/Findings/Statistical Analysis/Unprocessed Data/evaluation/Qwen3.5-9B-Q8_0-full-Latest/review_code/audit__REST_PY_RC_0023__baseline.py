import requests

def solve(inputs):
    """
    Searches for countries using the REST Countries v5 API based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip (for pagination).
            - search_text (str): Search term for country names or codes.
            - credential (str): Caller-supplied API key/credential.
    
    Returns:
        list | None: Decoded JSON response as a list, or None if the response is empty but successful.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://restcountries.com/v5.1/search"
    
    params = {
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"],
        "searchText": inputs["search_text"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP Error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response (e.g., no countries found)
    if not data:
        return None
    
    return data