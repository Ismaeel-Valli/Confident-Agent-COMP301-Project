import requests

def solve(inputs):
    """
    Updates a todo item in JSONPlaceholder with a new title and returns the updated ID.
    
    Args:
        inputs (dict): A dictionary containing:
            - resource_id (int): The ID of the todo to update.
            - new_title (str): The new title for the todo.
    
    Returns:
        int or None: The ID of the updated todo, or None if the response is empty.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    resource_id = inputs.get("resource_id")
    new_title = inputs.get("new_title")

    if resource_id is None or new_title is None:
        raise ValueError("Missing required input fields: resource_id and new_title.")

    url = f"{base_url}/todos/{resource_id}"
    payload = {"title": new_title}

    response = requests.patch(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update todo. Status code: {response.status_code}, Response: {response.text}")

    data = response.json()
    
    # JSONPlaceholder returns an empty object {} on successful PATCH for this endpoint in some versions/configs,
    # or the full updated object. The instructions say return None for a successful empty response.
    if not data:
        return None
    
    return data.get("id")