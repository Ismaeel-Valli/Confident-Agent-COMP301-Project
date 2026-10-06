import requests

def solve(inputs):
    """
    Update a post in JSONPlaceholder with a new body value.
    
    Args:
        inputs (dict): Dictionary containing:
            - resource_id (int): ID of the post to update
            - new_body (str): New body content
    
    Returns:
        str or None: The title field from the response, or None if absent/empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://jsonplaceholder.typicode.com"
    resource_id = inputs["resource_id"]
    new_body = inputs["new_body"]
    
    url = f"{base_url}/posts/{resource_id}"
    
    response = requests.put(url, json={"body": new_body})
    
    if response.status_code != 200:
        raise Exception(f"Failed to update post: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return data.get("title")