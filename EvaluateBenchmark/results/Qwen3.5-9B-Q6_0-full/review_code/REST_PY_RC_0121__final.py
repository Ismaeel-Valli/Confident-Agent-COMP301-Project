import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: Currency code to match exactly
            - results_to_skip: Number of results to skip
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    value = inputs["value"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    base_url = "https://api.restcountries.com/v5.0"
    url = f"{base_url}/currency/{value}"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Skip the specified number of results
    if isinstance(data, list):
        skipped_data = data[results_to_skip:]
        return skipped_data
    
    return None