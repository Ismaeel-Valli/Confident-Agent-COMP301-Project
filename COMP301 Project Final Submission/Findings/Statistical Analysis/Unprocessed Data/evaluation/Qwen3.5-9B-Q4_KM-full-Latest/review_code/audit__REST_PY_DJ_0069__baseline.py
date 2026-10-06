import requests

def solve(inputs):
    """
    Updates selected fields of a post on DummyJSON API.
    
    Args:
        inputs (dict): Contains 'resource_id' (post ID) and 'new_body' (new body content).
        
    Returns:
        None if the update is successful (empty response), otherwise returns the decoded JSON response.
        
    Raises:
        Exception for unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    new_body = inputs['new_body']
    
    url = f"https://jsonplaceholder.typicode.com/posts/{resource_id}"
    
    payload = {
        "body": new_body
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update post. Status code: {response.status_code}, Response: {response.text}")
    
    return None