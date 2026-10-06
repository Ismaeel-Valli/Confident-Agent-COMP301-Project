import requests

def solve(inputs):
    """
    Retrieve one page of countries from REST Countries v5 API.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return
            - results_to_skip (int): Number of results to skip (pagination)
            - included_attributes (list): List of attributes to include in response
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    
    # Build query parameters
    params = {
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"]
    }
    
    # Include credential in headers as assumed by the problem
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    # Make the API request
    response = requests.get(base_url, params=params, headers=headers)
    
    # Check for unsuccessful HTTP response
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code}")
    
    # Decode JSON response
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