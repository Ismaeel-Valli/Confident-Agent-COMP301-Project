import requests

def solve(inputs):
    """
    Search REST Countries v5 using caller-supplied credential.
    
    inputs: dict with keys:
      - results_to_skip (int): Number of results to skip (offset)
      - included_attributes (list[str]): Attributes to return only
      - search_text (str): Search term for country names
      - credential (str): API key/credential
    
    Returns:
      - list[dict]: Decoded JSON response if successful
      - None: If successful but empty response
      - Raises: Exception on unsuccessful HTTP response
    """
    base_url = "https://api.restcountries.com"
    endpoint = "/v5.2/search"
    
    params = {
        "search": inputs["search_text"],
        "skip": inputs["results_to_skip"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(f"{base_url}{endpoint}", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter to only included attributes if specified
    if inputs["included_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for attr in inputs["included_attributes"]:
                if attr in country:
                    filtered_country[attr] = country[attr]
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data