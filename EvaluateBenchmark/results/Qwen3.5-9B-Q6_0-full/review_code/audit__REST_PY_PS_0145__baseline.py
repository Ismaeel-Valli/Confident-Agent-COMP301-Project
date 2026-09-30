import requests
import json

def solve(inputs):
    """
    Adds a new pet to the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'credential': Authentication token or header value.
            - 'new_category': Category of the new pet.
            - 'new_resource_id': ID for the new pet.
            - 'new_name': Name of the new pet.
            - 'new_photo_links': List of photo URLs for the new pet.
            - 'new_tags': List of tags for the new pet.
    
    Returns:
        dict or None: Decoded JSON response from the API, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful status code.
    """
    # Base URL for Swagger Petstore OpenAPI 3 (public demo)
    BASE_URL = "https://petstore.swagger.io/v2"
    
    # Prepare the payload based on inputs
    payload = {
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "tags": inputs["new_tags"],
        "category": {
            "id": None,  # Assuming category ID is not provided or should be null; adjust if needed
            "name": inputs["new_category"]
        },
        "status": "available"  # Default status as per OpenAPI spec examples
    }
    
    # Set the resource ID in the payload if required by the specific implementation
    # Note: Standard Swagger Petstore v2 does not typically require an 'id' field in the request body,
    # but since the input provides 'new_resource_id', we include it.
    payload["id"] = inputs["new_resource_id"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {inputs['credential']}"  # Adjust based on actual auth mechanism (e.g., API Key)
    }

    try:
        response = requests.post(
            f"{BASE_URL}/pet",
            json=payload,
            headers=headers
        )
        
        # Raise an exception for unsuccessful HTTP responses (4xx, 5xx)
        response.raise_for_status()
        
        # Decode the JSON response
        decoded_response = response.json()
        
        # Return None for a successful empty response
        if not decoded_response:
            return None
        
        return decoded_response
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP Error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")