import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: Currency code to match exactly
            - results_to_skip: Number of results to skip
            - excluded_attributes: List of country attributes to exclude
            - credential: Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5"
    
    # Build query parameters
    params = {
        "currency": inputs["value"],
        "skip": inputs["results_to_skip"]
    }
    
    # Make the request with provided credential
    headers = {"Authorization": f"Bearer {inputs['credential']}"}
    response = requests.get(f"{base_url}/countries", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    # Filter out excluded attributes
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