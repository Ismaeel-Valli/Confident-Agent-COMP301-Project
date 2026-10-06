import requests

def solve(inputs):
    """
    Update selected fields of a post on DummyJSON.
    
    Args:
        inputs (dict): Contains 'resource_id' (post ID) and 'new_body' (new body text).
        
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    new_body = inputs['new_body']
    
    url = "https://dummyjson.com/posts/{id}".format(id=resource_id)
    
    payload = {
        "body": new_body
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.put(url, json=payload, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    return response.json()