import requests

def solve(inputs):
    """
    Update selected fields of a post on DummyJSON.
    
    Args:
        inputs (dict): Contains 'resource_id', 'new_body', and 'new_title'.
        
    Returns:
        int or None: The response's id value, or None if absent or successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/posts"
    resource_id = inputs["resource_id"]
    new_body = inputs["new_body"]
    new_title = inputs["new_title"]
    
    payload = {
        "title": new_title,
        "body": new_body
    }
    
    response = requests.put(f"{base_url}/{resource_id}", json=payload)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Check for id in the response
    if "id" in data and data["id"] is not None:
        return data["id"]
    
    # Return None for successful empty response or missing id
    return None