import requests

def solve(inputs):
    """
    Submits a new comment to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'new_body': The body text for the comment.
            - 'new_name': The name of the commenter.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, 
                      None if the response is empty but successful.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    url = "https://jsonplaceholder.typicode.com/comments"
    data = {
        "body": inputs["new_body"],
        "name": inputs["new_name"]
    }

    response = requests.post(url, json=data)
    
    if not response.ok:
        raise requests.exceptions.RequestException(f"Request failed with status code: {response.status_code}")

    if len(response.content) == 0:
        return None
    
    return response.json()