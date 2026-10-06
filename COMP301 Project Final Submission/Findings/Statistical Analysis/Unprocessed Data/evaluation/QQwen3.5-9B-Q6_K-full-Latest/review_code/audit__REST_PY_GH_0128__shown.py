import requests

def solve(inputs):
    """
    Update a GitHub release using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - release_id (int): Unique identifier of the release to update
            - new_name (str): New name for the release
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    release_id = inputs["release_id"]
    new_name = inputs["new_name"]
    credential = inputs["credential"]
    
    # GitHub REST API endpoint for updating a release
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/{release_id}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Update the release name using PATCH method
    payload = {
        "name": new_name
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Return decoded JSON response, or None if successful with empty response
    return response.json() if response.text else None