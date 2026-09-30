import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code.
    
    Args:
        inputs (dict): Dictionary containing:
            - value: Country code to match exactly (str)
            - results_to_skip: Number of results to skip (int)
            - excluded_attributes: List of attributes to exclude from response (list of str)
            - credential: Caller-supplied credential (str)
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5"
    endpoint = "/country/borders"
    url = f"{base_url}{endpoint}"
    
    params = {
        "borders": inputs["value"],
        "skip": inputs["results_to_skip"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Filter out excluded attributes
    if inputs["excluded_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {}
            for k, v in country.items():
                if k not in inputs["excluded_attributes"]:
                    filtered_country[k] = v
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data