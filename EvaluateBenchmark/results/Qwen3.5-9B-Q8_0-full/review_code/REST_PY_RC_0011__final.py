import requests

def solve(inputs):
    """
    Search REST Countries v5 by country codes using a search term.
    
    Args:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip (offset)
            - search_text (str): Search term for country names
            - credential (str): API key/credential
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5/search?search={inputs['search_text']}&skip={inputs['results_to_skip']}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return None if len(data) == 0 else data
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")