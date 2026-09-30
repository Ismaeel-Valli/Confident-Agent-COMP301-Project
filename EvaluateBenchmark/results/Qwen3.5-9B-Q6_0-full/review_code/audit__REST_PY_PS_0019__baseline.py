import requests

def solve(inputs):
    """
    Adds a new pet to the Swagger Petstore (OpenAPI 3) store.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'new_name' (str): The name for the new pet.
            - 'new_photo_links' (list or str): Photo URLs for the new pet.
            - 'credential' (str): Bearer token for authentication.
    
    Returns:
        str or None: The name of the newly created pet, or None if the response is empty/successful without a name.
    
    Raises:
        requests.exceptions.HTTPError: If the HTTP response status code indicates an error.
    """
    base_url = "https://petstore.swagger.io/v2"
    url = f"{base_url}/pet"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    # Prepare the payload based on OpenAPI 3 Pet schema expectations
    payload = {
        "name": inputs['new_name'],
        "photoUrls": inputs['new_photo_links'] if isinstance(inputs['new_photo_links'], list) else [inputs['new_photo_links']]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses (4xx, 5xx)
    response.raise_for_status()
    
    # Return the name if present in the response, otherwise None
    return response.json().get("name")