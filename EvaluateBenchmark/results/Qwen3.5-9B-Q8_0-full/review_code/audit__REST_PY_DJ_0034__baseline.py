import requests

def solve(inputs):
    """
    Retrieves one page of posts from DummyJSON based on the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing 'result_limit' (int).
        
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, 
                      None if successful but empty, or raises an exception on failure.
    """
    result_limit = inputs.get('result_limit')
    
    # DummyJSON endpoint for posts with limit
    url = f"https://jsonplaceholder.typicode.com/posts?_limit={result_limit}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # Return None if the response is empty (though unlikely with this API unless limit is 0)
        if not data:
            return None
            
        return data
        
    except requests.exceptions.HTTPError as errh:
        raise Exception(f"HTTP Error occurred: {errh}")
    except requests.exceptions.RequestException as err:
        raise Exception(f"Request failed: {err}")