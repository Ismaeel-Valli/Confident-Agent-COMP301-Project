import requests

def solve(inputs):
    """
    Searches for countries using the REST Countries v5 API based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip (for pagination).
            - search_text (str): Search term for country names or codes.
            - credential (str): Caller-supplied credential (e.g., API key) for authentication.
    
    Returns:
        dict or None: The decoded JSON response if results are found, or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code outside 200-299).
    """
    base_url = "https://restcountries.com/v3.1"
    params = {
        "search": inputs["search_text"],
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(f"{base_url}/country", params=params, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response (e.g., no countries found)
    if not data:
        return None
    
    return data