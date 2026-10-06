import requests

def solve(inputs):
    """
    Update selected fields of a post on DummyJSON.
    
    inputs:
        - resource_id: int, ID of the post to update
        - new_body: str, new value for the body attribute
        - new_title: str, new value for the title attribute
    
    Returns:
        - The decoded JSON response (or None if successful with empty response)
    
    Raises:
        Exception for unsuccessful HTTP responses
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
        raise Exception(f"Failed to update post: {response.status_code} - {response.text}")
    
    return None