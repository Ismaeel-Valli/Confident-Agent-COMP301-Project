import requests

def solve(inputs):
    """
    Retrieve one page of todos from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to return
            
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
        
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    # Base URL for DummyJSON todos
    base_url = "https://dummyjson.com/todos"
    
    try:
        # Make GET request to retrieve todos (no fields parameter as it's not documented)
        response = requests.get(base_url)
        
        # Raise exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode JSON response
        data = response.json()
        
        # Return None for successful empty response (empty todos array)
        if not data.get("todos") or len(data["todos"]) == 0:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")