import requests

def solve(inputs):
    """
    Retrieves one page of countries from REST Countries v5 API using provided credentials.
    
    Args:
        inputs (dict): A dictionary containing 'credential' key with necessary permissions.
        
    Returns:
        dict or None: Decoded JSON response, or None if the response is successfully empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    # Assuming the base URL for REST Countries v5 API
    base_url = "https://restcountries.com/v5.1"
    
    # Constructing the endpoint to retrieve countries (example: /countries)
    endpoint = "/countries"
    
    # Prepare headers with credentials
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    # Make the GET request
    response = requests.get(f"{base_url}{endpoint}", headers=headers)
    
    # Check if the HTTP response is successful (status code 200-299)
    if not response.ok:
        raise Exception(f"HTTP {response.status_code} error occurred while fetching countries.")
    
    # Decode the JSON response
    try:
        data = response.json()
    except ValueError as e:
        raise Exception(f"Failed to decode JSON response: {e}")
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data