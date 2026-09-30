import requests

def solve(inputs):
    """
    Update selected fields of a post on DummyJSON.
    
    Args:
        inputs (dict): Contains 'resource_id' (post ID) and 'new_body' (new body value).
        
    Returns:
        str or None: The title of the updated post, or None if absent or response is empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    resource_id = inputs['resource_id']
    new_body = inputs['new_body']
    
    base_url = "https://dummyjson.com/posts"
    url = f"{base_url}/{resource_id}"
    
    payload = {
        "body": new_body
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.put(url, json=payload, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Check for empty response
    if not data:
        return None
    
    # Return title if present, otherwise None
    return data.get('title')