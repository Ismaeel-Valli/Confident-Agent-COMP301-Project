import requests

def solve(inputs):
    """
    Adds a new pet to the Swagger Petstore (OpenAPI 3) store.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'new_category': str, value for the category attribute
            - 'new_resource_id': int or str, value for the id attribute
            - 'new_name': str, value for the name attribute
            - 'new_photo_links': list of str, value for the photoUrls attribute
            - 'credential': dict, containing necessary credentials (e.g., username/password)
    
    Returns:
        str or None: The 'name' value from the response if present, otherwise None.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    # Base URL for Swagger Petstore OpenAPI 3 (public demo server)
    base_url = "https://petstore.swagger.io/v2"
    
    # Prepare the payload
    pet_data = {
        "name": inputs["new_name"],
        "category": {"name": inputs["new_category"]},
        "photoUrls": inputs["new_photo_links"],
        "tags": [],  # Empty list as tags are optional and not provided
        "status": "available"  # Default status, commonly used in Petstore
    }
    
    # Set up headers with authentication if credentials are provided
    headers = {
        "Content-Type": "application/json"
    }
    
    credential = inputs.get("credential")
    if credential:
        username = credential.get("username")
        password = credential.get("password")
        if username and password:
            auth = requests.auth.HTTPBasicAuth(username, password)
            headers["Authorization"] = "Basic " + requests.auth._basic_auth_str(username, password)

    # Make the POST request to add the pet
    response = requests.post(
        f"{base_url}/pet",
        json=pet_data,
        auth=auth if credential and "username" in credential else None,
        headers=headers
    )
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Return the 'name' value from the response if present, otherwise None
    return response.json().get("name")