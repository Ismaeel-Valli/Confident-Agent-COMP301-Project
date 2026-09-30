import requests

def solve(inputs):
    """
    Update a post in JSONPlaceholder with new body content.
    
    Args:
        inputs (dict): Dictionary containing:
            - resource_id (int): ID of the post to update
            - new_body (str): New body content for the post
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://jsonplaceholder.typicode.com"
    resource_id = inputs["resource_id"]
    new_body = inputs["new_body"]
    
    url = f"{base_url}/posts/{resource_id}"
    
    payload = {
        "body": new_body
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code == 200:
        return None
    
    elif response.status_code == 201:
        return response.json()
    
    else:
        raise Exception(f"Failed to update post: {response.status_code} - {response.text}")