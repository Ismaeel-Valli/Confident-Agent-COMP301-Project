import requests

def solve(inputs):
    """
    Search country names on REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - included_attributes (list): List of attributes to include in the response.
            - search_text (str): Search term for country names.
            - credential (str): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com/v5"
    url = f"{base_url}/search?name={inputs['search_text']}&limit={inputs['result_limit']}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    # Filter to only include requested attributes
    filtered_data = []
    for item in data:
        filtered_item = {}
        for attr in inputs['included_attributes']:
            if attr in item:
                filtered_item[attr] = item[attr]
        filtered_data.append(filtered_item)
    
    return filtered_data if filtered_data else None