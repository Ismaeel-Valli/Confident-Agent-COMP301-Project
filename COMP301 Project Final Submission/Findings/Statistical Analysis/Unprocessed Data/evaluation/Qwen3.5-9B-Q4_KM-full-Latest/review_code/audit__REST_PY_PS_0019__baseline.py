import requests

def solve(inputs):
    """
    Adds a new pet to the Swagger Petstore (OpenAPI 3) store.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'new_name': The name for the new pet.
            - 'new_photo_links': A list of photo URLs for the new pet.
            - 'credential': Credentials (e.g., API key or token) for authentication.
    
    Returns:
        str or None: The 'name' attribute from the response if present, otherwise None.
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful status code.
    """
    # Base URL for Swagger Petstore OpenAPI 3 (example; adjust as needed)
    base_url = "https://petstore.swagger.io/v2"
    
    # Construct the payload based on OpenAPI 3 schema for adding a pet
    payload = {
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"] if isinstance(inputs["new_photo_links"], list) else [inputs["new_photo_links"]]
    }
    
    # Prepare headers with credentials (assuming 'credential' is an API key or token)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {inputs['credential']}"  # Adjust auth scheme if necessary
    }
    
    url = f"{base_url}/pet"
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Parse the response JSON
        response_data = response.json()
        
        # Return the 'name' attribute if present, otherwise None
        return response_data.get("name")
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Unsuccessful HTTP response: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")