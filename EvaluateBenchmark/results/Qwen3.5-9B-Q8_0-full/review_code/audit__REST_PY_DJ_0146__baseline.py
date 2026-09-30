import requests

def solve(inputs):
    """
    Retrieves one page of posts from DummyJSON based on provided sorting parameters.
    
    Args:
        inputs (dict): A dictionary containing:
            - sort_field (str): Field used for ordering.
            - sort_direction (str): Ordering direction ('asc' or 'desc').
    
    Returns:
        list or None: The decoded JSON response as a list of posts, or None if the response is empty.
    
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com/posts"
    
    # Construct query parameters
    params = {
        '_sort': inputs['sort_field'],
        '_order': inputs['sort_direction']
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # Return None if the response is empty (successful but no posts)
        if not data:
            return None
            
        return data
        
    except requests.RequestException as e:
        raise e