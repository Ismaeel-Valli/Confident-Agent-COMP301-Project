import requests

def solve(inputs):
    """
    Update an existing pet in the Swagger Petstore API.
    
    Parameters:
        inputs (dict): Contains:
            - 'credential': Authentication token/credential string
            - 'new_category': Category value for the pet
            - 'new_resource_id': ID of the pet to update
            - 'new_name': Name value for the pet
            - 'new_photo_links': Photo URLs list or single URL
            - 'new_tags': Tags list
    
    Returns:
        int or None: HTTP status code from response, or None if absent.
                     Returns None also for successful empty responses (204).
    
    Raises:
        Exception: For unsuccessful HTTP responses (non-2xx).
    """
    base_url = "https://petstore3.swagger.io/api/v3"
    endpoint = "/pet"
    url = f"{base_url}{endpoint}"
    
    # Build the payload for PUT request
    payload = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "category": {"name": inputs["new_category"]},
        "photoUrls": inputs["new_photo_links"] if isinstance(inputs["new_photo_links"], list) else [inputs["new_photo_links"]],
        "tags": inputs["new_tags"] if isinstance(inputs["new_tags"], list) else [{"name": inputs["new_tags"]}] if isinstance(inputs["new_tags"], str) else []
    }
    
    # Handle case where tags might be a single string or already a list of dicts
    if isinstance(inputs["new_tags"], str):
        payload["tags"] = [{"name": inputs["new_tags"]}]
    elif not isinstance(inputs["new_tags"], list):
        payload["tags"] = []
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.put(url, json=payload, headers=headers)
        
        # Raise exception for unsuccessful HTTP responses (non-2xx)
        if not 200 <= response.status_code < 300:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        # Return status code or None if absent
        return response.status_code if "status" in response.json() else None
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")