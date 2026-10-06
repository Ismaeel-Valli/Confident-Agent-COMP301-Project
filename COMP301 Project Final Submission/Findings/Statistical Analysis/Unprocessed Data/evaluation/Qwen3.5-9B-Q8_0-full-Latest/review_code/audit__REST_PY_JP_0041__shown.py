import requests

def solve(inputs):
    """
    Update a post in JSONPlaceholder with a new title.
    
    Args:
        inputs (dict): Contains 'resource_id' and 'new_title'.
        
    Returns:
        int or None: The updated post's id, or None if the response is empty.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    resource_id = inputs["resource_id"]
    new_title = inputs["new_title"]
    
    url = f"{base_url}/posts/{resource_id}"
    payload = {"title": new_title}
    
    response = requests.put(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return data.get("id")
    elif response.status_code == 204:
        return None
    else:
        raise requests.RequestException(f"Failed to update post: {response.status_code}")