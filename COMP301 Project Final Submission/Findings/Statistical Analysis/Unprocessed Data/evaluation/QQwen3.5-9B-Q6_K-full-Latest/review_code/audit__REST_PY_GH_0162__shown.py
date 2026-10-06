import requests


def solve(inputs):
    """
    Create a release on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - new_body (str): Value for the body attribute
            - new_tag_name (str): Value for the tag name attribute
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    body = inputs["new_body"]
    tag_name = inputs["new_tag_name"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    data = {
        "tag_name": tag_name,
        "name": tag_name,
        "body": body
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to create release: {response.status_code} - {response.text}")
    
    return response.json() if response.content else None