import requests

def solve(inputs):
    """
    Retrieve a post by identifier from JSONPlaceholder and return its title.
    
    Args:
        inputs (dict): Must contain 'resource_id' (int) identifying the post.
        
    Returns:
        str or None: The post's title, or None if absent or response is empty.
        
    Raises:
        requests.RequestException: For unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    url = "https://jsonplaceholder.typicode.com/posts"
    
    try:
        response = requests.get(url, params={"postId": resource_id})
        response.raise_for_status()  # Raises exception for non-2xx status
        
        data = response.json()
        
        # Return title if present, else None
        return data.get("title")
    except requests.RequestException:
        raise