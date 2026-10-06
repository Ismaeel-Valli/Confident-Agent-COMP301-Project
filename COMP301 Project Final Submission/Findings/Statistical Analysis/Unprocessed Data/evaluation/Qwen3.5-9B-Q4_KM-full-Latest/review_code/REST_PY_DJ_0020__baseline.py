import requests

def solve(inputs):
    """
    Retrieves a todo by identifier from DummyJSON.
    
    Args:
        inputs (dict): A dictionary containing 'resource_id' as the todo identifier.
        
    Returns:
        dict or None: The decoded JSON response if successful and data exists, 
                      None if the response is successfully empty.
                      
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    resource_id = inputs['resource_id']
    
    # DummyJSON endpoint to get a specific todo by ID
    url = f"https://dummyjson.com/todos/{resource_id}"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            # If the response contains an empty todos list or null, return None
            if not data.get('todos') and not data.get('todo'):
                return None
            return data
        else:
            raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")