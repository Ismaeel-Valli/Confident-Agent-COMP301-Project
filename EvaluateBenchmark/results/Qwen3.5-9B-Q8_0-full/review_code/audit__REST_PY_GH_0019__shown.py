import requests

def solve(inputs):
    """
    Update an issue comment on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - comment_id (int): The unique identifier of the comment.
            - new_body (str): The new body content for the comment.
            - credential (str): The caller-supplied authentication token.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, otherwise None.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    # Construct the API URL for updating an issue comment
    base_url = "https://api.github.com/repos"
    url = f"{base_url}/{inputs['repository_owner']}/{inputs['repository_name']}/issues/comments/{inputs['comment_id']}"
    
    # Prepare the headers with authentication
    headers = {
        "Authorization": f"token {inputs['credential']}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Prepare the request body
    payload = {
        "body": inputs['new_body']
    }
    
    # Send the PATCH request to update the comment
    response = requests.patch(url, json=payload, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data