import requests

def solve(inputs):
    """
    Search REST Countries v5 by country codes using the provided search term.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results to return.
            - search_text (str): Search term for country names or codes.
            - credential (str): Caller-supplied API key/credential.
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5/search?search={inputs['search_text']}&limit={inputs['result_limit']}"
    
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