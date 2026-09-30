import requests

def solve(inputs):
    """
    Updates a GitHub release using the REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - release_id (str): The unique identifier of the release.
            - new_body (str): The new value for the body attribute of the release.
            - credential (dict): Caller-supplied credential information (e.g., token).
    
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful status code.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    release_id = inputs["release_id"]
    new_body = inputs["new_body"]
    credential = inputs["credential"]
    
    # Construct the API URL for updating a release
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/{release_id}"
    
    # Prepare headers with authentication
    headers = {
        "Authorization": f"token {credential.get('token', '')}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Prepare the payload for updating the release body
    payload = {
        "body": new_body
    }
    
    # Send the PATCH request to update the release
    response = requests.patch(url, headers=headers, json=payload)
    
    # Check if the response is successful (status code 200-299)
    if response.status_code < 300:
        # Return None for a successful empty response
        if not response.text.strip():
            return None
        # Otherwise, return the decoded JSON response
        return response.json()
    else:
        # Raise an exception for an unsuccessful HTTP response
        raise Exception(f"Failed to update release: {response.status_code} - {response.text}")