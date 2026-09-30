import requests

def solve(inputs):
    """
    Retrieve one page of todos from DummyJSON and return the decoded JSON response.
    
    Parameters:
        inputs (dict): A dictionary containing 'page' key with an integer value.
        
    Returns:
        list or None: The decoded JSON response as a list, or None if the response is empty.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    page = inputs.get('page', 1)
    base_url = "https://dummyjson.com"
    endpoint = "/todos"
    
    url = f"{base_url}{endpoint}?page={page}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        todos = data.get('todos', [])
        
        if not todos:
            return None
        
        return todos
    
    except requests.exceptions.RequestException as e:
        raise e