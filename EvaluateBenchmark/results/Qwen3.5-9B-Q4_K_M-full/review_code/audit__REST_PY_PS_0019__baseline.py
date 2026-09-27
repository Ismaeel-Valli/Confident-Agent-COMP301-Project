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
        str or None: The name of the newly added pet if present in the response, 
                     or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful status code.
    """
    # Swagger Petstore OpenAPI 3 base URL (public version)
    BASE_URL = "https://petstore.swagger.io/v2"
    
    # Construct the pet object based on OpenAPI 3 schema for /pet
    new_pet = {
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"]
    }
    
    # Prepare headers with credentials. 
    # Assuming 'credential' is an API key or token to be passed in Authorization header.
    # Adjusting based on common Swagger Petstore auth methods (e.g., Bearer token or custom header).
    # Since the problem states "caller-supplied credential", we'll assume it's a Bearer token 
    # or an API key that goes into a specific header. A common pattern for Swagger Petstore is 
    # using an 'Authorization' header with 'Bearer <token>' or similar. 
    # However, without explicit schema of the credential, we'll try a generic approach.
    # If the credential is an API key, it might go in 'x-api-key'. 
    # Given the ambiguity, we'll assume it's a Bearer token for now, but this can be adjusted.
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {inputs['credential']}"  # Adjust if credential is an API key instead
    }
    
    url = f"{BASE_URL}/pet"
    
    try:
        response = requests.post(url, json=new_pet, headers=headers)
        
        # Check for unsuccessful HTTP status code
        if response.status_code >= 400:
            raise Exception(f"Failed to add pet. Status code: {response.status_code}, Response: {response.text}")
        
        # Return the name from the response if present
        if "name" in response.json():
            return response.json()["name"]
        else:
            return None
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error occurred while adding pet: {str(e)}")