import requests

def solve(inputs):
    """
    Finds a pet by ID in the Swagger Petstore (OpenAPI 3 service) and returns its name.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'pet_identifier' (int): The ID of the pet to find.
            - 'credential' (str): The API key or token for authentication.
    
    Returns:
        str or None: The name of the pet if found, otherwise None.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://petstore3.swagger.io/api/v3/openapi.yaml"  # Placeholder; actual endpoint may vary
    
    # Assuming the API endpoint for getting a pet by ID is /pet/{petId}
    url = f"https://petstore3.swagger.io/api/v3/pet/{inputs['pet_identifier']}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        if response.status_code == 200:
            data = response.json()
            return data.get('name')
        elif response.status_code == 204:
            return None
        else:
            raise Exception(f"Unexpected status code: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        raise e