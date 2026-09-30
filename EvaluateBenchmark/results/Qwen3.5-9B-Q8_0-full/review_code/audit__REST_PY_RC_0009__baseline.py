import requests

def solve(inputs):
    """
    Retrieves one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'results_to_skip' (int): Number of results to skip.
            - 'credential' (str): Caller-supplied credential (API key).
    
    Returns:
        dict or None: Decoded JSON response, or None if the response is successfully empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://restcountries.com/v5.1"
    endpoint = "/data/countries"
    
    params = {
        'skip': inputs['results_to_skip'],
        'limit': 100  # Assuming a reasonable page size; can be adjusted if needed
    }
    
    headers = {
        'Authorization': f'Bearer {inputs["credential"]}'
    }
    
    response = requests.get(f"{base_url}{endpoint}", params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return None if not data else data
    else:
        raise Exception(f"HTTP request failed with status code {response.status_code}: {response.text}")