import requests

def solve(inputs):
    """
    Search REST Countries v5 by text.
    
    inputs:
        result_limit (int): Maximum number of results.
        included_attributes (list[str]): Attributes to include in response.
        search_text (str): Search term.
        credential (str): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
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
    
    data = response.json()
    
    if not data:
        return None
    
    # Filter to only included attributes if specified
    if inputs['included_attributes']:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for attr in inputs['included_attributes']:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data