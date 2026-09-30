import requests

def solve(inputs):
    """
    Finds a pet by ID using the Swagger Petstore (OpenAPI 3) API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'pet_identifier': The ID of the pet to retrieve.
            - 'credential': The caller-supplied credential for authentication.
    
    Returns:
        str or None: The 'name' value from the response if present, otherwise None.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code >= 400).
    """
    pet_identifier = inputs['pet_identifier']
    credential = inputs['credential']
    
    # Base URL for Swagger Petstore OpenAPI 3
    base_url = "https://petstore3.swagger.io/api/v3"
    
    # Construct the endpoint to get a pet by ID
    url = f"{base_url}/pet/{pet_identifier}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    # Check if the response is empty (no content)
    if not response.content:
        return None
    
    # Parse the JSON response
    try:
        data = response.json()
    except ValueError:
        # If the response is not JSON, return None or handle as needed
        return None
    
    # Return the 'name' attribute if it exists, otherwise None
    return data.get('name')