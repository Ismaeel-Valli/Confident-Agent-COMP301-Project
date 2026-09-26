```python
import requests

def solve(inputs):
    """
    Retrieves posts from JSONPlaceholder using the provided inputs (though typically 
    no specific input filtering is needed for a basic 'get all posts' request).
    
    Args:
        inputs (dict): A dictionary that may contain optional parameters like 'userId', 
                       though this function will fetch all posts by default.
    
    Returns:
        list or None: The decoded JSON response as a list of posts, or None if the 
                      response is an empty list.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails (non-2xx status).
    """
    # Base URL for JSONPlaceholder API
    base_url = "https://jsonplaceholder.typicode.com"
    
    # Construct the endpoint for posts. 
    # Note: The 'inputs' parameter is accepted but not strictly used here to fetch all posts.
    # If specific filtering (like userId) was intended, it could be added to the URL query params.
    url = f"{base_url}/posts"
    
    try:
        response = requests.get(url)
        
        # Raise an exception for unsuccessful HTTP responses (non-2xx status codes)
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None for a successful empty response
        if not data:
            return None
            
        return data
        
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to retrieve posts from JSONPlaceholder: {e}")
```