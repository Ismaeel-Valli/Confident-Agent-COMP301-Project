import requests

def solve(inputs):
    """
    Deletes a pet from the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): A dictionary containing:
            - 'pet_identifier': The ID of the pet to delete.
            - 'credential': The caller-supplied credential (e.g., API key or token) for authentication.
    
    Returns:
        int: The successful HTTP status code (typically 204 No Content).
    
    Raises:
        requests.exceptions.RequestException: If an unsuccessful HTTP response is received.
    """
    # Base URL for Swagger Petstore OpenAPI 3
    base_url = "https://petstore.swagger.io/v2"
    
    # Extract inputs
    pet_id = inputs['pet_identifier']
    credential = inputs['credential']
    
    # Construct the delete endpoint URL
    url = f"{base_url}/pet/{pet_id}"
    
    # Prepare headers with the provided credential
    # Assuming 'credential' is an API key or Bearer token. Adjust based on actual Swagger Petstore auth method.
    # For standard Swagger Petstore, it often uses Basic Auth or a specific header like 'x-api-key'.
    # Since the problem states "caller-supplied credential", we'll assume it's passed in a standard way.
    # Common practice for such tasks: if it's an API key, use 'X-API-Key'; if Bearer, use 'Authorization'.
    # Given the ambiguity, we'll try a generic approach often used in these challenges: Basic Auth or X-API-Key.
    # However, without specific instruction on credential format, let's assume it's an API key for 'x-api-key' header
    # as that's common in OpenAPI 3 examples when not using OAuth flow explicitly in the snippet.
    # If the credential is a username/password tuple, we'd use basic_auth parameter.
    # Let's assume 'credential' is a string representing an API key for now, as it's simpler and common in these contexts.
    headers = {'X-API-Key': credential} if isinstance(credential, str) else {}
    
    try:
        response = requests.delete(url, headers=headers)
        # Raise an exception for unsuccessful HTTP responses (4xx, 5xx)
        response.raise_for_status()
        return response.status_code
    except requests.exceptions.HTTPError as e:
        # Re-raise the exception if the response was not successful
        raise e