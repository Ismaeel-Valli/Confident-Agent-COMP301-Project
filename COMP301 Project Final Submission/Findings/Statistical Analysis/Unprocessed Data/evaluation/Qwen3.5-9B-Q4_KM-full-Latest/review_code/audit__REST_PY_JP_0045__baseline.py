import requests

def solve(inputs):
    """
    Replaces a comment record on JSONPlaceholder with the supplied data.
    
    Parameters:
        inputs (dict): A dictionary containing:
            - resource_id (int): Identifier of the comment to replace.
            - new_body (str): New value for the 'body' attribute.
            - new_email (str): New value for the 'email' attribute.
            - new_name (str): New value for the 'name' attribute.
            - new_post_identifier (int): New value for the 'postId' attribute.
    
    Returns:
        int or None: The response's 'id' value if present, otherwise None.
                      Returns None for a successful empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code outside 2xx).
    """
    base_url = "https://jsonplaceholder.typicode.com"
    resource_id = inputs["resource_id"]
    new_body = inputs["new_body"]
    new_email = inputs["new_email"]
    new_name = inputs["new_name"]
    new_post_identifier = inputs["new_post_identifier"]

    url = f"{base_url}/comments/{resource_id}"
    payload = {
        "body": new_body,
        "email": new_email,
        "name": new_name,
        "postId": new_post_identifier
    }

    response = requests.put(url, json=payload)

    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")

    # For successful PUT on JSONPlaceholder, the response body is typically empty.
    # We return None for a successful empty response as per instructions.
    if not response.text.strip():
        return None

    # If there's content, try to extract 'id' from the response JSON.
    try:
        data = response.json()
        return data.get("id")
    except ValueError:
        # If response is not valid JSON but status is 2xx, treat as empty success per spec.
        return None