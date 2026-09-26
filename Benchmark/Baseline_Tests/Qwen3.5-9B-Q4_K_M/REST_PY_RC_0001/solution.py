import requests

def solve(inputs):
    """
    Retrieves one page of countries from REST Countries v5 API using provided credentials.
    
    Args:
        inputs (dict): A dictionary containing 'credential' key with necessary permissions.
        
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    url = "https://restcountries.com/v5/all"
    credential = inputs["credential"]
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return data if data else None