import requests

def solve(inputs):
    """
    Search REST Countries v5 by country codes using provided inputs.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results to return.
            - excluded_attributes (list): List of attributes to exclude from results.
            - search_text (str): Search term for country names or codes.
            - credential (str): Caller-supplied authentication token.
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5/search?search={inputs['search_text']}&limit={inputs['result_limit']}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter out excluded attributes from each country object
    filtered_data = []
    for country in data:
        filtered_country = {}
        for key, value in country.items():
            if key not in inputs['excluded_attributes']:
                filtered_country[key] = value
        filtered_data.append(filtered_country)
    
    # Return None if the result is empty (successful but no results)
    if len(filtered_data) == 0:
        return None
    
    return filtered_data