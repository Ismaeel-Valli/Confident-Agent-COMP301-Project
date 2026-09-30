import requests

def solve(inputs):
    """
    Adds a new pet to the Swagger Petstore (OpenAPI 3) store.
    
    Args:
        inputs (dict): A dictionary containing:
            - new_resource_id (str or int): Value for the 'id' attribute.
            - new_name (str): Value for the 'name' attribute.
            - new_photo_links (list of str): Value for the 'photoUrls' attribute.
            - new_tags (list of dict): Value for the 'tags' attribute.
            - credential (dict): Caller-supplied credentials (e.g., API key or token).
    
    Returns:
        The response's 'id' value if present, otherwise None for a successful empty response.
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful status code.
    """
    
    # Swagger Petstore OpenAPI 3 base URL (using the public demo server)
    BASE_URL = "https://petstore.swagger.io/v2"
    
    # Construct the payload based on the inputs provided
    payload = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "tags": inputs["new_tags"],
        "status": "available"  # Default status as per OpenAPI spec if not provided
    }
    
    # Prepare headers with credentials (assuming 'credential' contains an API key or token)
    # Adjust header key based on actual Swagger Petstore auth method (e.g., 'x-api-key')
    headers = {
        "Content-Type": "application/json"
    }
    
    # If credential is a dict, extract the appropriate key/token; otherwise use as-is
    if isinstance(inputs["credential"], dict):
        # Common pattern for Swagger Petstore: using x-api-key or Authorization header
        if "api_key" in inputs["credential"]:
            headers["x-api-key"] = inputs["credential"]["api_key"]
        elif "token" in inputs["credential"]:
            headers["Authorization"] = f"Bearer {inputs['credential']['token']}"
        else:
            # Fallback: assume the entire credential dict is meant to be passed somehow, 
            # but for this function we'll just use a generic key if present
            pass
    else:
        # If credential is not a dict, assume it's an API key string
        headers["x-api-key"] = inputs["credential"]
    
    endpoint = f"{BASE_URL}/pet"
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Return the 'id' from the response if present
        if "id" in response.json():
            return response.json()["id"]
        else:
            # For a successful empty response, return None
            return None
            
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Failed to add pet: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error occurred: {e}")