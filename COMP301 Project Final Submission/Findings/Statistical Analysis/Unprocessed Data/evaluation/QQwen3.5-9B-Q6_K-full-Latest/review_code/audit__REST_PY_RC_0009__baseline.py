import requests

def solve(inputs):
    """
    Retrieves one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'results_to_skip' (int): Number of results to skip.
            - 'credential' (str): Caller-supplied credential (API key).
    
    Returns:
        dict or None: The decoded JSON response, or None if the response is empty.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://restcountries.com/v5.1/all"
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 10  # Assuming one page means a default limit, adjust if needed
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code}")
    
    data = response.json()
    
    return data if data else None