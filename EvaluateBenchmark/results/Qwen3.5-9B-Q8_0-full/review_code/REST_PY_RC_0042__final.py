import requests

def solve(inputs):
    """
    Search country names using REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results
            - results_to_skip (int): Number of results to skip
            - included_attributes (list): Attributes to include in response
            - search_text (str): Search term for country names
            - credential (str): API credential
    
    Returns:
        dict or None: Decoded JSON response, or None if empty but successful
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v3.1"
    
    params = {
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"],
        "fields": ",".join(inputs["included_attributes"]),
        "search": inputs["search_text"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return None if len(data) == 0 else data