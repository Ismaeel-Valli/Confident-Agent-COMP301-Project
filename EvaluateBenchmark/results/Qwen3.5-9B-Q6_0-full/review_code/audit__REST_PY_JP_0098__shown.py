import requests

def solve(inputs):
    """
    Submit a new todo to JSONPlaceholder using the provided inputs.
    
    Parameters:
        inputs (dict): Dictionary containing:
            - 'new_completed' (bool): Value for the completed attribute
            - 'new_title' (str): Value for the title attribute
    
    Returns:
        dict or None: Decoded JSON response, or None if successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/todos"
    
    payload = {
        "title": inputs["new_title"],
        "completed": inputs["new_completed"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create todo. Status code: {response.status_code}")
    
    return response.json()