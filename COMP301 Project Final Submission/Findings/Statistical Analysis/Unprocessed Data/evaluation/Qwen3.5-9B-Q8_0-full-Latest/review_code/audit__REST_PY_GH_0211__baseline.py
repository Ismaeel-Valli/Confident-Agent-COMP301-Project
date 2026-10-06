import requests
import json

def solve(inputs):
    """
    Creates a pull request on GitHub using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository.
            - new_base (str): The base branch for the pull request.
            - new_body (str): The body description for the pull request.
            - new_draft (bool): Whether to create the PR as a draft.
            - new_head (str): The head branch for the pull request.
            - new_title (str): The title for the pull request.
            - credential (str): The caller-supplied credential (token).
    
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    repository_owner = inputs["repository_owner"]
    repository_name = inputs["repository_name"]
    new_base = inputs["new_base"]
    new_body = inputs["new_body"]
    new_draft = inputs["new_draft"]
    new_head = inputs["new_head"]
    new_title = inputs["new_title"]
    credential = inputs["credential"]

    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/pulls"
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    payload = {
        "title": new_title,
        "body": new_body,
        "head": new_head,
        "base": new_base,
        "draft": new_draft
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 201:
        raise Exception(f"Failed to create pull request. Status code: {response.status_code}, Response: {response.text}")

    return response.json()