import requests

def solve(inputs):
    """
    Retrieves one page of todos from DummyJSON based on skip count and included fields.
    
    Args:
        inputs (dict): Dictionary containing:
            - results_to_skip (int): Number of results to skip.
            - included_fields (str): Comma-separated list of fields to include.
    
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com"  # Using a real public API for demonstration; DummyJSON doesn't have a stable /todos endpoint with these params in the same way.
    # However, since the prompt specifically mentions "DummyJSON", we will construct the request to match typical DummyJSON behavior if it existed, 
    # but since DummyJSON's actual structure differs, we'll adapt to a realistic scenario using jsonplaceholder as a proxy for the logic, 
    # OR strictly follow the instruction to use "DummyJSON" by pointing to its known structure.
    
    # Correction: The user asked for "DummyJSON". DummyJSON has an endpoint like /api/todos but it doesn't support 'skip' and 'fields' in the same way as RESTful APIs with pagination.
    # Given the ambiguity, I will implement the logic assuming a hypothetical DummyJSON API that supports these parameters at '/todos'.
    # If DummyJSON is strictly the one at https://dummyjson.com/, its todos endpoint is GET /todos and doesn't support 'skip' or 'fields' directly in the query string for filtering fields.
    # To adhere strictly to the prompt's intent (even if the real API might not support it exactly), we will construct the URL with these params.
    
    url = f"https://dummyjson.com/todos?skip={inputs['results_to_skip']}&limit=10&fields={inputs['included_fields']}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # DummyJSON returns a dict with 'todos' key. If the list is empty, we return None as per instruction.
        if not data.get('todos'):
            return None
            
        return data
        
    except requests.exceptions.HTTPError as errh:
        raise Exception(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        raise Exception(f"Connection Error: {errc}")
    except requests.exceptions.Timeout as errt:
        raise Exception(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        raise Exception(f"Request Error: {err}")