import requests

def solve(inputs):
    """
    Replaces an album record in JSONPlaceholder with supplied data.
    
    Args:
        inputs (dict): Dictionary containing:
            - resource_id (int): ID of the album to update.
            - new_title (str): New title for the album.
            - new_user_identifier (int): New user ID for the album.
    
    Returns:
        str or None: The 'title' value from the response JSON, or None if absent or on success with empty body.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    resource_id = inputs['resource_id']
    new_title = inputs['new_title']
    new_user_identifier = inputs['new_user_identifier']

    payload = {
        "id": resource_id,
        "title": new_title,
        "userId": new_user_identifier,
        "albumId": 1  # Keeping albumId as a placeholder since it's required by the schema
    }

    response = requests.put(
        f"{base_url}/albums/{resource_id}",
        json=payload
    )

    if response.status_code != 200:
        raise Exception(f"Failed to update album. Status code: {response.status_code}, Response: {response.text}")

    return response.json().get("title")