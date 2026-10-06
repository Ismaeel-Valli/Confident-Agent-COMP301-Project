import requests

def solve(inputs):
    """
    Updates an existing pet in the Swagger Petstore (OpenAPI 3 service) 
    with new attributes provided in the inputs dictionary.
    
    Parameters:
        inputs (dict): Contains the following keys:
            - 'credential': Authentication token or credentials.
            - 'new_category': New category value for the pet.
            - 'new_resource_id': ID of the pet to update.
            - 'new_name': New name for the pet.
            - 'new_photo_links': List of photo URLs for the pet.
            - 'new_status': New status for the pet.
    
    Returns:
        str or None: The 'name' attribute from the response if present, otherwise None.
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful operation.
    """
    base_url = "https://petstore.swagger.io/v2"
    pet_id = inputs['new_resource_id']
    credential = inputs['credential']

    # Prepare the payload for updating the pet
    update_data = {
        "name": inputs.get('new_name'),
        "category": {"id": None, "name": inputs.get('new_category')},
        "photoUrls": inputs.get('new_photo_links', []),
        "tags": [],
        "status": inputs.get('new_status')
    }

    # Make the PUT request to update the pet
    response = requests.put(
        f"{base_url}/pet/{pet_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {credential}"}
    )

    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()

    # Extract and return the 'name' from the response if present
    try:
        return response.json().get('name')
    except ValueError:
        return None