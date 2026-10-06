import requests

def solve(inputs):
    """
    Submits a new todo to JSONPlaceholder with the provided title.
    
    Args:
        inputs (dict): A dictionary containing 'new_title' for the todo's title.
        
    Returns:
        str or None: The response's title value if present, otherwise None for an empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    url = "https://jsonplaceholder.typicode.com/todos"
    
    payload = {
        "userId": 1,
        "title": inputs["new_title"],
        "completed": False
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create todo. Status code: {response.status_code}")
        
    data = response.json()
    
    if not data:
        return None
        
    return data.get("title")