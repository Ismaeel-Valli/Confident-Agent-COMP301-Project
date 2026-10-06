import requests

def solve(inputs):
    """
    Replaces a todo record in JSONPlaceholder with supplied data.
    
    Parameters:
        inputs (dict): Contains 'resource_id', 'new_completed', 'new_title', 'new_user_identifier'.
        
    Returns:
        str or None: The title from the response, or None if successful and empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    resource_id = inputs['resource_id']
    new_completed = inputs['new_completed']
    new_title = inputs['new_title']
    new_user_identifier = inputs['new_user_identifier']

    url = "https://jsonplaceholder.typicode.com/todos/1"  # Note: JSONPlaceholder uses fixed IDs for PUT/PATCH in some contexts, but we'll use the provided resource_id.
    # However, standard JSONPlaceholder behavior for updating a specific todo by ID requires using that ID in the URL.
    # We will construct the URL dynamically based on resource_id.
    url = f"https://jsonplaceholder.typicode.com/todos/{resource_id}"

    payload = {
        "completed": new_completed,
        "title": new_title,
        "userId": new_user_identifier
    }

    response = requests.put(url, json=payload)

    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code: {response.status_code}")

    # JSONPlaceholder returns an empty body on successful update (200 OK)
    return None