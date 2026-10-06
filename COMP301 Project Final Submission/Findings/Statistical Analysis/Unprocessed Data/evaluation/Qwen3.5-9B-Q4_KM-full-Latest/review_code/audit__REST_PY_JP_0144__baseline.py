import requests

def solve(inputs):
    """
    Submits a new todo to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'new_title': The title for the new todo.
            - 'new_user_identifier': The userId for the new todo.
    
    Returns:
        int or None: The id of the created todo, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (non-2xx status code).
    """
    url = "https://jsonplaceholder.typicode.com/todos"
    payload = {
        "title": inputs["new_title"],
        "userId": inputs["new_user_identifier"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    # Check for empty response body
    if not response.text.strip():
        return None
    
    try:
        data = response.json()
        return data.get("id")
    except ValueError:
        # If JSON parsing fails but we got a successful status, treat as no id found
        return None