import requests

def solve(inputs):
    """
    Look up countries by exact match on their region using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - "value": The region value to match exactly
            - "credential": Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    region = inputs["value"]
    credential = inputs["credential"]
    
    url = f"{base_url}/v5/region/{region}"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return None if len(data) == 0 else data