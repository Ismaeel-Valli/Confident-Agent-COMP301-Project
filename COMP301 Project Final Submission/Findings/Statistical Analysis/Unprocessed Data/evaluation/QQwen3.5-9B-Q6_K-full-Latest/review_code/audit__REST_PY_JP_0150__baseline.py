import requests

def solve(inputs):
    """
    Submits a new comment to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'new_body': The body content for the new comment.
            - 'new_name': The name for the new comment.
            
    Returns:
        str or None: The 'name' value from the response if present, otherwise None.
                     Returns None for a successful empty response.
                     
    Raises:
        requests.RequestException: If the HTTP request is unsuccessful.
    """
    url = "https://jsonplaceholder.typicode.com/comments"
    
    payload = {
        "body": inputs["new_body"],
        "name": inputs["new_name"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise requests.RequestException(f"Failed to submit comment. Status code: {response.status_code}")
    
    return response.json().get("name")