import requests

def solve(inputs):
    """
    Search REST Countries v5 by text, skipping a number of results.
    
    Args:
        inputs (dict): Must contain:
            - results_to_skip (int): Number of results to skip.
            - search_text (str): Search term for country names.
            - credential (str): API key for authentication.
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5/search?name={inputs['search_text']}&skip={inputs['results_to_skip']}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return None if len(data) == 0 else data
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")