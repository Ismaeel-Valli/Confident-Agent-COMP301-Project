import requests

def solve(inputs):
    """
    Replace a comment record in JSONPlaceholder with supplied data.
    
    Inputs:
        resource_id (int): Identifier of the comment to replace.
        new_body (str): New value for the body attribute.
        new_email (str): New value for the email attribute.
        new_name (str): New value for the name attribute.
        new_post_identifier (int): New value for the post_id attribute.
    
    Returns:
        dict or None: The decoded JSON response, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/comments/{inputs['resource_id']}"
    
    payload = {
        "body": inputs["new_body"],
        "email": inputs["new_email"],
        "name": inputs["new_name"],
        "postId": inputs["new_post_identifier"]
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    return response.json() if response.content else None