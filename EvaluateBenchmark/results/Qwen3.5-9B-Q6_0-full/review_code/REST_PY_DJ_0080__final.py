import requests

def solve(inputs):
    """
    Update selected fields of a post on DummyJSON.
    
    Args:
        inputs (dict): Contains 'resource_id' (post ID) and 'new_body' (new body value).
        
    Returns:
        int or None: The response's id value, or None if absent or successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/posts"
    resource_id = inputs.get("resource_id")
    new_body = inputs.get("new_body")
    
    payload = {
        "id": resource_id,
        "body": new_body
    }
    
    response = requests.patch(f"{base_url}/{resource_id}", json=payload)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Check for success indicators in the response
    if "id" not in data or data.get("id") is None:
        return None
    
    return data["id"]