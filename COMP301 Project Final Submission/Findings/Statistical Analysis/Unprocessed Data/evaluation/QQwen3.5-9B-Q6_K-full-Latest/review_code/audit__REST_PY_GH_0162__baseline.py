import requests
import json

def solve(inputs):
    """
    Creates a release on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - new_body (str): Value for the body attribute.
            - new_tag_name (str): Value for the tag name attribute.
            - credential (str): Caller-supplied authentication token.
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    repository_owner = inputs["repository_owner"]
    repository_name = inputs["repository_name"]
    new_body = inputs["new_body"]
    new_tag_name = inputs["new_tag_name"]
    credential = inputs["credential"]

    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/releases"
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    data = {
        "tag_name": new_tag_name,
        "body": new_body
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        return None
    elif response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to create release. Status code: {response.status_code}, Response: {response.text}")