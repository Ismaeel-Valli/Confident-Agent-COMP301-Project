import requests

def solve(inputs):
    """
    Update a pull request on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - pull_number (int): Pull request number
            - new_body (str): New body content for the PR
            - new_title (str): New title for the PR
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.github.com"
    version = "2026-03-10"
    
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    pr_number = inputs["pull_number"]
    new_body = inputs["new_body"]
    new_title = inputs["new_title"]
    credential = inputs["credential"]
    
    url = f"{base_url}/repos/{owner}/{repo}/pulls/{pr_number}"
    
    headers = {
        "Accept": f"application/vnd.github.{version}-preview+json",
        "Authorization": f"Bearer {credential}"
    }
    
    payload = {
        "title": new_title,
        "body": new_body
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to update pull request: {response.status_code} - {response.text}")
    
    return response.json() if response.status_code != 204 else None