import requests

def solve(inputs):
    """
    Replaces a post record in JSONPlaceholder with supplied data.
    
    Args:
        inputs (dict): Dictionary containing:
            - resource_id (int): Identifier of the post to update.
            - new_body (str): New value for the body attribute.
            - new_title (str): New value for the title attribute.
            - new_user_identifier (int): New value for the user Id attribute.
    
    Returns:
        int or None: The response's id value if present, otherwise None for a successful empty response.
    
    Raises:
        requests.RequestException: If the HTTP response is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    resource_id = inputs['resource_id']
    new_body = inputs['new_body']
    new_title = inputs['new_title']
    new_user_identifier = inputs['new_user_identifier']

    payload = {
        "id": resource_id,
        "title": new_title,
        "body": new_body,
        "userId": new_user_identifier
    }

    try:
        response = requests.put(f"{base_url}/posts/{resource_id}", json=payload)
        response.raise_for_status()
        
        if response.status_code == 204:
            return None
        
        data = response.json()
        return data.get('id')
    
    except requests.RequestException as e:
        raise e