import requests

def solve(inputs):
    """
    Search REST Countries v5 using provided inputs.
    
    Args:
        inputs (dict): Contains:
            - result_limit (int): Maximum number of results
            - results_to_skip (int): Number of results to skip
            - included_attributes (list): Attributes to include in response
            - search_text (str): Search term
            - credential (str): API key/credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5"
    
    params = {
        "limit": inputs["result_limit"],
        "skip": inputs["results_to_skip"],
        "search": inputs["search_text"]
    }
    
    # Map included_attributes to the API's query parameters if needed
    # For now, we'll pass them as a comma-separated string if the API supports it
    if inputs["included_attributes"]:
        params["attributes"] = ",".join(inputs["included_attributes"])
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.get(
        f"{base_url}/countries",
        params=params,
        headers=headers
    )
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data