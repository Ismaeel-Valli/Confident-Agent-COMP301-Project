import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their bordering country code using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The country code to match exactly for borders.
            - 'results_to_skip': Number of results to skip (offset).
            - 'excluded_attributes': List of attributes to exclude from the response.
            - 'credential': API key/credential for authentication.
    
    Returns:
        dict or None: Decoded JSON response. Returns None if the response is successfully empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (non-2xx status code).
    """
    base_url = "https://restcountries.com/v5.1"
    endpoint = "/geography/borders"
    
    value = inputs.get("value")
    results_to_skip = inputs.get("results_to_skip", 0)
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs.get("credential")
    
    if not credential:
        raise ValueError("Credential is required in inputs.")

    params = {
        "code": value,
        "skip": results_to_skip,
        "exclude": ",".join(excluded_attributes) if excluded_attributes else None
    }

    headers = {
        "Authorization": f"Bearer {credential}"
    }

    response = requests.get(f"{base_url}{endpoint}", params=params, headers=headers)

    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"HTTP request failed with status code: {response.status_code}. Response body: {response.text}")

    data = response.json()

    # If the response is an empty list, return None as per requirement for successful empty response
    if isinstance(data, list) and len(data) == 0:
        return None

    return data