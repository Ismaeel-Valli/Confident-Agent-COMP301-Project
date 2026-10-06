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
        Exception: If the HTTP request is unsuccessful.
    """
    # Construct the API URL for updating an issue comment
    base_url = "https://api.github.com"
    version = "2026-03-10"
    url = f"{base_url}/repos/{inputs['repository_owner']}/{inputs['repository_name']}/issues/comments/{inputs['comment_id']}"
    
    # Prepare the headers with authentication
    headers = {
        "Authorization": f"token {inputs['credential']}",
        "Accept": f"application/vnd.github.{version}-preview+json",
        "Content-Type": "application/json"
    }
    
    # Prepare the request body
    payload = {
        "body": inputs['new_body']
    }
    
    # Make the PATCH request to update the comment
    response = requests.patch(url, headers=headers, json=payload)
    
    # Check if the request was successful (status code 200-299)
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failed to update issue comment. Status code: {response.status_code}, Response: {response.text}")
    
    # Decode the JSON response
    response_data = response.json()
    
    # Return None for a successful empty response (though GitHub typically returns the updated comment)
    if not response_data:
        return None
    
    return response_data