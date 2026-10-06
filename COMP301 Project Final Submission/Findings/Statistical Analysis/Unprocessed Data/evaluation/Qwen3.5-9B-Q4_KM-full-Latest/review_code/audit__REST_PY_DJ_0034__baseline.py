import requests

def solve(inputs):
    """
    Retrieves one page of posts from DummyJSON based on the provided inputs.
    
    Parameters:
        inputs (dict): A dictionary containing 'result_limit' for maximum number of results.
        
    Returns:
        list or None: The decoded JSON response as a list of posts, or None if the response is empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com/posts"
    
    # Prepare headers and query parameters
    params = {
        "_limit": inputs.get("result_limit", 10)
    }
    
    try:
        response = requests.get(base_url, params=params)
        
        # Raise an exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None if the response is empty (though DummyJSON typically returns a list)
        return data if data else None
        
    except requests.exceptions.HTTPError as errh:
        raise Exception(f"HTTP Error: {errh}")
    except requests.exceptions.RequestException as err:
        raise Exception(f"Request Error: {err}")