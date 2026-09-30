import requests
import json

def solve(inputs):
    """
    Retrieves one page of countries from REST Countries v5 API using provided credentials.
    
    Args:
        inputs (dict): A dictionary containing 'credential' key with necessary permissions.
        
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
        
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    # Assuming the API endpoint and authentication method based on REST Countries v5 standards
    # Note: Actual implementation depends on specific API documentation which isn't provided here.
    # This is a template assuming a typical authenticated GET request pattern.
    
    base_url = "https://restcountries.com/v3.1/all"  # Example endpoint, adjust as needed
    
    # Prepare headers with credential information
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(base_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            # Return None for empty successful response
            return None if len(data) == 0 else data
        elif response.status_code == 401 or response.status_code == 403:
            raise Exception(f"Authentication failed with status code {response.status_code}")
        else:
            raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")