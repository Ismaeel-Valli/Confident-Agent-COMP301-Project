```python
import requests
import json

def solve(inputs):
    """
    Updates an existing pet in the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing:
            - new_resource_id (str): The new ID for the pet.
            - new_name (str): The new name for the pet.
            - new_photo_links (list of str): The new photo URLs for the pet.
            - credential (dict): Caller-supplied credentials (e.g., API key or token).
    
    Returns:
        dict or None: The decoded JSON response from the server, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful status code.
    """
    # Base URL for Swagger Petstore (OpenAPI 3) - assuming standard public instance
    base_url = "https://petstore.swagger.io/v2"
    
    # Construct the payload for updating the pet
    payload = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"]
    }
    
    # Determine the endpoint and method
    # Assuming we are updating an existing pet by ID, which is typically a PUT request to /pet/{petId}
    # However, since the input provides a new_resource_id, we will use that as the path parameter.
    # Note: In OpenAPI 3, 'id' is often read-only and not updatable via standard update endpoints, 
    # but per the problem statement, we proceed with updating the pet using the provided ID.
    
    endpoint = f"/pet/{inputs['new_resource_id']}"
    url = f"{base_url}{endpoint}"
    
    # Prepare headers for authentication (assuming Bearer token or API key in credential)
    # Adjust based on actual credential structure; here we assume a common pattern.
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {inputs['credential'].get('token', inputs['credential'].get('api_key', ''))}"
    }
    
    try:
        response = requests.put(url, json=payload, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Decode the JSON response
        response_data = response.json()
        
        # Return None if the response is empty (though JSONDecodeError might occur if body is empty string)
        if not response_data:
            return None
        
        return response_data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP Error occurred while updating pet: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"A request error occurred while updating pet: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to decode JSON response: {e}")
```