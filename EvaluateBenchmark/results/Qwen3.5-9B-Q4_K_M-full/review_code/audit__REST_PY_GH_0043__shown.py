import requests

def solve(inputs):
    """
    Create a release on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - new_tag_name (str): Tag name for the release
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    tag = inputs["new_tag_name"]
    token = inputs["credential"]
    
    url = "https://api.github.com/repos/{owner}/{repo}/releases"
    url = url.format(owner=owner, repo=repo)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    data = {
        "tag_name": tag,
        "name": tag,
        "body": "",
        "draft": False,
        "prerelease": False
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create release. Status code: {response.status_code}, Response: {response.text}")
    
    return response.json()