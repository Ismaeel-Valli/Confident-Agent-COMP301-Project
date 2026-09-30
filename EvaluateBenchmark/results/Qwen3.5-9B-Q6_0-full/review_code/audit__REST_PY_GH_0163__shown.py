import requests

def solve(inputs):
    """
    Update a GitHub release using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): The account owner of the repository
            - repository_name (str): The name of the repository without .git extension
            - release_id (int): The unique identifier of the release
            - new_body (str): Value for the body attribute
            - credential (str): Caller-supplied authentication token
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    release_id = inputs["release_id"]
    new_body = inputs["new_body"]
    credential = inputs["credential"]
    
    # GitHub API endpoint for updating a release
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/{release_id}"
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    data = {
        "body": new_body
    }
    
    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to update release: {response.status_code} - {response.text}")
    
    # Return decoded JSON response
    return response.json()