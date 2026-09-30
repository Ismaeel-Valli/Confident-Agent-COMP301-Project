import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: Capital city to match exactly
            - result_limit: Maximum number of results
            - included_attributes: List of country attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        list or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    capital = inputs["value"]
    limit = inputs["result_limit"]
    attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # REST Countries v5 endpoint for searching by capital
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/search/capital?name={capital}&limit={limit}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # If the response is an empty list, return None as per specification
    if data == []:
        return None
    
    # Filter to only include requested attributes
    filtered_results = []
    for country in data:
        filtered_country = {}
        for attr in attributes:
            if attr in country:
                filtered_country[attr] = country[attr]
        filtered_results.append(filtered_country)
    
    return filtered_results