import requests

def solve(inputs):
    """
    Updates a todo item in JSONPlaceholder with a new title and returns the updated title.
    
    Parameters:
        inputs (dict): A dictionary containing:
            - 'resource_id' (int): The ID of the todo to update.
            - 'new_title' (str): The new title for the todo.
    
    Returns:
        str or None: The updated title if present, otherwise None.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    resource_id = inputs['resource_id']
    new_title = inputs['new_title']
    
    url = "https://jsonplaceholder.typicode.com/todos/1"  # Note: JSONPlaceholder doesn't support PUT for partial updates in the same way as REST APIs with dynamic IDs. However, we'll assume a hypothetical endpoint or use PATCH if supported. Since JSONPlaceholder does not officially support PATCH, this function will simulate a PUT request to update the todo.
    
    # Construct the URL dynamically based on resource_id
    url = f"https://jsonplaceholder.typicode.com/todos/{resource_id}"
    
    payload = {
        "title": new_title
    }
    
    try:
        response = requests.put(url, json=payload)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses
        
        if response.status_code == 204:
            return None
        
        data = response.json()
        return data.get('title')
    
    except requests.exceptions.RequestException as e:
        raise e