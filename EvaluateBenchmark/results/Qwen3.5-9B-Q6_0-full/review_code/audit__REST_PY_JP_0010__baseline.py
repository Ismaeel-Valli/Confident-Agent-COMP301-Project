import requests

def solve(inputs):
    """
    Replaces a comment record on JSONPlaceholder with the supplied data.
    
    Args:
        inputs (dict): A dictionary containing:
            - resource_id (int): Identifier of the comment to update.
            - new_body (str): New value for the body attribute.
            - new_email (str): New value for the email attribute.
            - new_name (str): New value for the name attribute.
            - new_post_identifier (int): New value for the postId attribute.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, otherwise None.
    
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/comments/{inputs['resource_id']}"
    
    payload = {
        "body": inputs["new_body"],
        "email": inputs["new_email"],
        "name": inputs["new_name"],
        "postId": inputs["new_post_identifier"]
    }

    response = requests.put(url, json=payload)
    response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

    if response.status_code == 204:
        return None
    
    return response.json()