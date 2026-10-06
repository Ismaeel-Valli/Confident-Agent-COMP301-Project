import requests

def solve(inputs):
    """
    Update selected fields of a post on DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - resource_id (int): Identifier of the post to update.
            - new_body (str): New value for the body attribute.
    
    Returns:
        str or None: The title value from the response, or None if absent or successful empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/posts"
    resource_id = inputs["resource_id"]
    new_body = inputs["new_body"]
    
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
    
    # Check if the response has a 'title' field
    if "title" in data and data["title"] is not None:
        return data["title"]
    else:
        return None