import requests

def solve(inputs):
    """
    Search country names using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - results_to_skip (int): Number of results to skip (offset)
            - excluded_attributes (list): Attributes to exclude from response
            - search_text (str): Search term for country names
            - credential (str): API credential/token
    
    Returns:
        dict or None: Decoded JSON response, or None if empty but successful
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5.0"
    
    params = {
        "search": inputs["search_text"],
        "skip": inputs["results_to_skip"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(f"{base_url}/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter out excluded attributes if any
    if inputs["excluded_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for key, value in country.items():
                if key not in inputs["excluded_attributes"]:
                    filtered_country[key] = value
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data