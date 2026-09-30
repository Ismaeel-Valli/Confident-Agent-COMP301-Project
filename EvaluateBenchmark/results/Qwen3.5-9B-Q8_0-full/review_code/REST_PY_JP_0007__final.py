import requests

def solve(inputs):
    """
    Retrieve comments from JSONPlaceholder using the provided inputs.
    
    Parameters:
        inputs (dict): A dictionary containing 'post_id' to fetch comments for a specific post.
        
    Returns:
        list or None: The decoded JSON response as a list of comments, or None if the response is empty.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    post_id = inputs.get("post_id")
    
    url = f"{base_url}/posts/{post_id}/comments"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise requests.RequestException(f"Failed to retrieve comments. Status code: {response.status_code}")
    
    data = response.json()
    
    return data if data else None