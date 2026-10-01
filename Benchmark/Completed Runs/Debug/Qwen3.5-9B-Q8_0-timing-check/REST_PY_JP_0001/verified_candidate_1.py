import requests

def solve(inputs):
    """
    Retrieve posts from JSONPlaceholder and return decoded JSON response.
    
    Args:
        inputs (dict): Must contain 'post_id' key for the endpoint.
        
    Returns:
        dict or None: Decoded JSON response, or None if empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    
    # Construct the URL based on inputs
    post_id = inputs.get('post_id')
    url = f"{base_url}/posts/{post_id}"
    
    # Make the GET request
    response = requests.get(url)
    
    # Raise exception for unsuccessful HTTP responses
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Return None for empty response, otherwise return the data
    if data is None or (isinstance(data, list) and len(data) == 0):
        return None
    
    return data