def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Parameters:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip (offset)
            - excluded_attributes (list): List of country attributes to exclude
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
    base_url = "https://api.restcountries.com/v5"
    url = f"{base_url}/countries?skip={inputs['results_to_skip']}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter out excluded attributes from each country
    if inputs['excluded_attributes']:
        filtered_countries = []
        for country in data:
            filtered_country = {}
            for key, value in country.items():
                if key not in inputs['excluded_attributes']:
                    filtered_country[key] = value
            filtered_countries.append(filtered_country)
        data = filtered_countries
    
    # Return None for successful empty response
    if len(data) == 0:
        return None
    
    return data