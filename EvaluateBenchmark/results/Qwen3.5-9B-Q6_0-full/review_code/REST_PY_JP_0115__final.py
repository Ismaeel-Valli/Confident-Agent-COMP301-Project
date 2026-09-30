def solve(inputs):
    """
    Update a post in JSONPlaceholder with new body content.
    
    Args:
        inputs (dict): Must contain 'resource_id' and 'new_body'.
        
    Returns:
        str or None: The title of the updated post, or None if absent/empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
    resource_id = inputs['resource_id']
    new_body = inputs['new_body']
    
    url = f"https://jsonplaceholder.typicode.com/posts/{resource_id}"
    
    payload = {
        'id': resource_id,
        'title': 'Updated Title',
        'body': new_body,
        'userId': 1
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    return data.get('title')