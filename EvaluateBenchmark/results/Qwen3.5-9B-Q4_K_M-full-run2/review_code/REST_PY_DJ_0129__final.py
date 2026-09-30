import requests

def solve(inputs):
    """
    Update selected fields of a post on DummyJSON.
    
    Inputs:
        inputs['resource_id']: Identifier of the post (int)
        inputs['new_body']: Value for the body attribute (str)
        inputs['new_title']: Value for the title attribute (str)
    
    Returns:
        The decoded JSON response, or None for a successful empty response.
    
    Raises:
        Exception for an unsuccessful HTTP response.
    """
    base_url = "https://dummyjson.com/posts"
    resource_id = inputs["resource_id"]
    new_body = inputs["new_body"]
    new_title = inputs["new_title"]
    
    payload = {
        "id": resource_id,
        "title": new_title,
        "body": new_body
    }
    
    response = requests.put(f"{base_url}/{resource_id}", json=payload)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    return response.json()