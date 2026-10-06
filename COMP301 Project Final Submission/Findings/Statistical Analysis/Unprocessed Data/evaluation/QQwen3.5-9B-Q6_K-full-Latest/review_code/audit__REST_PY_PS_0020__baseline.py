import requests

def solve(inputs):
    """
    Finds a pet by ID in the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'pet_identifier': The ID of the pet to retrieve.
            - 'credential': Caller-supplied credentials (assumed to have necessary permissions).
    
    Returns:
        str or None: The name of the pet if found, otherwise None for a successful empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://petstore.swagger.io/v2"
    pet_id = inputs["pet_identifier"]
    credential = inputs["credential"]
    
    # Construct the URL for fetching a specific pet by ID
    url = f"{base_url}/pet/{pet_id}"
    
    # Prepare headers with credentials (assuming 'credential' is an API key or token)
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Check if the response is empty (successful but no data)
        if not response.text.strip():
            return None
        
        # Parse the JSON response and extract the 'name' attribute
        pet_data = response.json()
        name = pet_data.get("name")
        
        return name
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Unsuccessful HTTP response: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")