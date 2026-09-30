import requests
import json

def solve(inputs):
    """
    Retrieves pet inventories by status from the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing 'credential' for authentication.
        
    Returns:
        list or None: Decoded JSON response as a list of pets, or None if the response is empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful (status code >= 400).
    """
    # Swagger Petstore OpenAPI 3 base URL for getting pet inventory by status
    url = "https://petstore.swagger.io/v2/pet/findByStatus"
    
    # Prepare headers with Bearer token from inputs["credential"]
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None if the response is empty (successful but no data)
        if not data:
            return None
            
        return data
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Unsuccessful HTTP response: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")