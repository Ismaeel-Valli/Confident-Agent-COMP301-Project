import requests

def solve(inputs):
    """
    Search REST Countries v5 using a caller-supplied credential.
    
    Parameters:
        inputs (dict): Must contain:
            - result_limit (int): Maximum number of results to return.
            - excluded_attributes (list[str]): Attributes to exclude from each country object.
            - search_text (str): Search term for the query.
            - credential (str): API key/credential with necessary permissions.
    
    Returns:
        list[dict] or None: Decoded JSON response. Returns None if successful but empty.
    
    Raises:
        requests.HTTPError: If the HTTP response indicates an unsuccessful status code.
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/search"
    url = f"{base_url}{endpoint}"
    
    params = {
        "search": inputs["search_text"],
        "limit": inputs["result_limit"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
    
    # Exclude specified attributes from each country object
    excluded = set(inputs["excluded_attributes"])
    filtered_data = []
    for country in data:
        filtered_country = {k: v for k, v in country.items() if k not in excluded}
        filtered_data.append(filtered_country)
    
    return filtered_data