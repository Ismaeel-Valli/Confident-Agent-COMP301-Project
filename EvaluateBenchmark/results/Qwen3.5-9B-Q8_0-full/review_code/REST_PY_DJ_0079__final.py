import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON, sorted by sort_field.
    
    Args:
        inputs (dict): Must contain 'sort_field' key.
        
    Returns:
        list or None: Decoded JSON response (list of posts), or None if empty.
        
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    sort_field = inputs.get('sort_field')
    
    # DummyJSON posts endpoint with sorting
    url = "https://dummyjson.com/posts"
    params = {'sort': sort_field}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises HTTPError for unsuccessful responses
        
        data = response.json()
        
        # Return the posts list, or None if empty
        return data.get('posts')
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")