import requests

def solve(inputs):
    """
    Updates a pull request in a GitHub repository using the REST API.
    
    Parameters:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - pull_number (int): The number identifying the pull request.
            - new_state (str): The new state for the pull request ('open', 'closed', or 'merged').
            - new_title (str): The new title for the pull request.
            - credential (dict): Caller-supplied credentials with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response if successful, None for an empty successful response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    repository_owner = inputs["repository_owner"]
    repository_name = inputs["repository_name"]
    pull_number = inputs["pull_number"]
    new_state = inputs["new_state"]
    new_title = inputs["new_title"]
    credential = inputs["credential"]

    # Construct the API URL for GitHub REST API version 2026-03-10
    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/pulls/{pull_number}"

    # Prepare headers with authentication
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    # Add authentication if provided (assuming credential contains 'token' or similar)
    if isinstance(credential, dict):
        token = credential.get("token") or credential.get("access_token")
        if token:
            headers["Authorization"] = f"Bearer {token}"

    # Prepare the payload for updating the pull request
    data = {
        "state": new_state,
        "title": new_title
    }

    # Send PATCH request to update the pull request
    response = requests.patch(url, json=data, headers=headers)

    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()

    # Return decoded JSON response or None if empty
    return response.json() if response.text else None