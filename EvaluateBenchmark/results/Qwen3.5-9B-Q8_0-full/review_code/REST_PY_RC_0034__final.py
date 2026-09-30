import requests

def solve(inputs):
    """
    Search country names on REST Countries v5 API.
    
    Parameters:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip.
            - included_attributes (list): List of attributes to include in the response.
            - search_text (str): Search term for country names.
            - credential (str): Caller-supplied credential (assumed valid).
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5/search/name"
    url = f"{base_url}{endpoint}"
    
    params = {
        "search": inputs["search_text"],
        "skip": inputs["results_to_skip"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter attributes as requested
    if inputs["included_attributes"]:
        filtered_data = []
        for item in data.get("data", []):
            filtered_item = {}
            for attr in inputs["included_attributes"]:
                if attr in item:
                    filtered_item[attr] = item[attr]
            filtered_data.append(filtered_item)
        return filtered_data
    
    return data if data else None