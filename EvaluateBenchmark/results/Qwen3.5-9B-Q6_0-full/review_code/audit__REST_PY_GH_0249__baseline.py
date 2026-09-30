import requests
from urllib.parse import quote

def solve(inputs):
    """
    Creates a new issue in a GitHub repository using the GitHub REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository.
            - new_assignees (list): List of assignee usernames or URLs.
            - new_body (str): The body text of the issue.
            - new_labels (list): List of label names or URLs.
            - new_title (str): The title of the issue.
            - credential (dict): Caller-supplied credentials containing 'token'.
    
    Returns:
        dict or None: The decoded JSON response if successful, None for empty response.
    
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    assignees = inputs["new_assignees"]
    body = inputs["new_body"]
    labels = inputs["new_labels"]
    title = inputs["new_title"]
    credential = inputs["credential"]["token"]
    
    url = f"https://api.github.com/repos/{quote(owner)}/{quote(repo)}/issues"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
        "Content-Type": "application/json"
    }
    
    data = {
        "title": title,
        "body": body,
        "assignees": assignees if assignees else [],
        "labels": labels if labels else []
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 201:
        response.raise_for_status()
    
    return response.json() if response.text else None