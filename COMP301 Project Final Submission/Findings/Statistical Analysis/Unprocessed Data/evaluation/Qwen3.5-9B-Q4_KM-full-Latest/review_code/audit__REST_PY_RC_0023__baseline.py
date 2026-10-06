import requests

def solve(inputs):
    """
    Searches for countries using REST Countries v5 API based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip (for pagination).
            - search_text (str): Search term for country names.
            - credential (str): Caller-supplied credential (e.g., API key or token).
    
    Returns:
        dict or None: Decoded JSON response if successful, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx range).
    """
    base_url = "https://restcountries.com/v3.1"
    endpoint = "search"
    
    params = {
        "search": inputs["search_text"],
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}" if inputs['credential'].startswith("Bearer ") else inputs['credential']
    }

    url = f"{base_url}/{endpoint}"
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return None if not data else data
    else:
        raise Exception(f"HTTP request failed with status code {response.status_code}: {response.text}")