import requests

def solve(inputs):
    """
    Adds a new pet to the Swagger Petstore (OpenAPI 3) store.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'new_resource_id': The ID for the new pet.
            - 'new_name': The name of the new pet.
            - 'new_photo_links': List of photo URLs for the new pet.
            - 'credential': Credentials (e.g., API key or token) for authentication.
    
    Returns:
        int or None: The status code of the response if present, otherwise None.
                      Returns None specifically if the response body is empty and successful.
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful status (4xx or 5xx).
    """
    # Base URL for Swagger Petstore OpenAPI 3
    base_url = "https://petstore.swagger.io/v2"
    endpoint = "/pet"
    url = f"{base_url}{endpoint}"

    # Prepare the payload based on OpenAPI 3 Pet schema
    payload = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"]
        # Note: 'category', 'tags', and 'status' are optional in many implementations.
        # We omit them as they are not provided in the inputs.
    }

    # Prepare headers for authentication (assuming Bearer token or API key based on common practice)
    # If 'credential' is a dict with 'token' or 'key', we adjust accordingly.
    # Assuming 'credential' is a string token for Authorization header.
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {inputs['credential']}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # Check if the response is successful (2xx status code)
        if 200 <= response.status_code < 300:
            # If the response body is empty, return None as per instructions
            if not response.text.strip():
                return None
            return response.status_code
        else:
            # Raise an exception for unsuccessful HTTP responses (4xx, 5xx)
            raise Exception(f"HTTP {response.status_code}: {response.text}")
            
    except requests.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")