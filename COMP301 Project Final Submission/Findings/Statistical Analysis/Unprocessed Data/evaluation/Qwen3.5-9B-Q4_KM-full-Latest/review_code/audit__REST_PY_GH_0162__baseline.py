import requests
import json

def solve(inputs):
    """
    Creates a release on GitHub using the REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - new_body (str): Value for the body attribute of the release.
            - new_tag_name (str): Value for the tag name attribute.
            - credential (dict): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    body = inputs["new_body"]
    tag = inputs["new_tag_name"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential['token']}",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    data = {
        "tag_name": tag,
        "body": body
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create release. Status code: {response.status_code}, Response: {response.text}")
    
    return response.json() if response.content else None