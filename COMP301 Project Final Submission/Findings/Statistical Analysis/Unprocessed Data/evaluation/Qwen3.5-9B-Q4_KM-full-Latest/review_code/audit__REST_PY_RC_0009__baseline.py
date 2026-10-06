import requests

def solve(inputs):
    """
    Retrieves one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'results_to_skip' (int): Number of results to skip for pagination.
            - 'credential' (str): Caller-supplied credential (e.g., API key or token).
    
    Returns:
        dict or None: The decoded JSON response if successful, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code outside 200-299).
    """
    base_url = "https://restcountries.com/v5"
    endpoint = "/geonames"  # Example endpoint; adjust if a specific one is intended.
    
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 100  # Assuming a reasonable page size; can be adjusted.
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}" if inputs['credential'].startswith("Bearer ") else inputs['credential']
    }
    
    response = requests.get(f"{base_url}{endpoint}", params=params, headers=headers)
    
    if not (200 <= response.status_code < 300):
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return None if len(data) == 0 else data