import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their subregion using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The subregion value to match exactly.
            - 'excluded_attributes': A list of country attributes to exclude from the response.
            - 'credential': The caller-supplied credential (e.g., API key or token).
    
    Returns:
        dict or None: The decoded JSON response if successful. Returns None for an empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    value = inputs["value"]
    excluded_attributes = inputs.get("excluded_attributes", [])
    credential = inputs["credential"]
    
    # Construct the query parameters
    params = {
        "subregion": value,
        "exclude": ",".join(excluded_attributes) if excluded_attributes else None
    }
    
    # Remove None values from params to avoid passing empty keys
    params = {k: v for k, v in params.items() if v is not None}
    
    url = "https://restcountries.com/v3.1/subregion"
    
    headers = {
        "Authorization": f"Bearer {credential}" if credential.startswith("Bearer ") else f"{credential}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for an empty successful response
    if not data:
        return None
    
    return data