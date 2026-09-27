import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their subregion using the REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The subregion value to match exactly.
            - 'result_limit': Maximum number of results to return.
            - 'results_to_skip': Number of results to skip (for pagination).
            - 'credential': Caller-supplied credential (e.g., API key or token).
    
    Returns:
        list|None: Decoded JSON response as a list of country objects, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code outside 200-299).
    """
    value = inputs["value"]
    result_limit = inputs["result_limit"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]

    # Construct the query parameters
    params = {
        "subregion": value,
        "limit": result_limit,
        "skip": results_to_skip
    }

    # Assuming a base URL for REST Countries v5; adjust if necessary.
    # Example: https://restcountries.com/v3.1/ (Note: 'v5' might be a typo or internal version; 
    # the public API is typically v3.1. If there's a specific v5 endpoint, replace accordingly.)
    base_url = "https://restcountries.com/v3.1"
    
    url = f"{base_url}/region"

    headers = {
        "Authorization": f"Bearer {credential}" if credential.startswith("Bearer ") else f"Token {credential}",
        # If the credential is an API key, it might need to be passed differently (e.g., as a query param or header).
        # Adjust based on the actual authentication method required by the specific v5 endpoint.
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")

    data = response.json()

    # Return None for a successful empty response
    if not data:
        return None

    return data