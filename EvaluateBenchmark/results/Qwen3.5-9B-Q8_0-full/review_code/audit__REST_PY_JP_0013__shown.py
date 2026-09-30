import requests

def solve(inputs):
    """
    Retrieve albums from JSONPlaceholder and return the decoded JSON response.
    
    Parameters:
        inputs (dict): A dictionary containing 'post_id' key with an integer value.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for empty response.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    
    # Construct the URL with the post_id parameter
    url = f"{base_url}/posts/{inputs['post_id']}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses
        
        data = response.json()
        
        # Return None if the response is empty (though this endpoint typically returns a single post object)
        if not data:
            return None
            
        return data
        
    except requests.exceptions.RequestException as e:
        raise e