import requests
import json

def solve(inputs):
    """
    Adds a new pet to the Swagger Petstore (OpenAPI 3) store.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'new_category': str, value for the category attribute
            - 'new_resource_id': int or str, value for the id attribute
            - 'new_name': str, value for the name attribute
            - 'new_photo_links': list of str, value for the photoUrls attribute
            - 'new_tags': list of dict (each with 'id' and 'name'), value for the tags attribute
            - 'credential': dict or tuple containing auth info (e.g., {'username': ..., 'password': ...} 
                            or ('user', 'pass') for basic auth)
    
    Returns:
        None if the response is successfully empty.
        The decoded JSON response if it contains data.
    
    Raises:
        Exception for unsuccessful HTTP responses.
    """
    
    # Construct the pet object based on OpenAPI 3 Petstore schema
    pet = {
        "name": inputs["new_name"],
        "id": inputs["new_resource_id"],
        "category": {"name": inputs["new_category"]},
        "photoUrls": inputs["new_photo_links"],
        "tags": inputs["new_tags"],
        "status": "available"  # Default status as per common OpenAPI Petstore examples
    }

    # Prepare authentication from the credential input
    auth = None
    if isinstance(inputs["credential"], dict):
        auth = requests.auth.HTTPBasicAuth(
            inputs["credential"].get("username", ""),
            inputs["credential"].get("password", "")
        )
    elif isinstance(inputs["credential"], tuple) and len(inputs["credential"]) == 2:
        auth = requests.auth.HTTPBasicAuth(inputs["credential"][0], inputs["credential"][1])

    # Make the POST request to add the pet
    url = "https://petstore.swagger.io/v2/pet"
    response = requests.post(url, json=pet, auth=auth)

    if response.status_code != 200:
        raise Exception(f"Failed to add pet. HTTP Status Code: {response.status_code}, Response: {response.text}")

    # Return None for empty successful response, else return decoded JSON
    if not response.content:
        return None
    return response.json()