import requests
from urllib.parse import quote

def solve(inputs):
    """
    Creates an issue in a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - new_assignees (list or str): Value for the assignees attribute.
            - new_body (str): Value for the body attribute.
            - new_labels (list or str): Value for the labels attribute.
            - new_title (str): Value for the title attribute.
            - credential (dict): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: The decoded JSON response. Returns None for a successful empty response.
    
    Raises:
        Exception: For an unsuccessful HTTP response.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    assignees = inputs["new_assignees"]
    body = inputs["new_body"]
    labels = inputs["new_labels"]
    title = inputs["new_title"]
    credential = inputs["credential"]
    
    # Construct the URL for creating an issue
    url = f"https://api.github.com/repos/{quote(owner)}/{quote(repo)}/issues"
    
    # Prepare headers with Bearer token authentication
    headers = {
        "Authorization": f"Bearer {credential['token']}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
        "Content-Type": "application/json"
    }
    
    # Prepare the payload for creating an issue
    payload = {
        "title": title,
        "body": body
    }
    
    # Handle assignees if provided
    if assignees:
        if isinstance(assignees, str):
            payload["assignees"] = [assignees]
        else:
            payload["assignees"] = assignees
    
    # Handle labels if provided
    if labels:
        if isinstance(labels, str):
            payload["labels"] = [labels]
        else:
            payload["labels"] = labels
    
    # Make the POST request to create the issue
    response = requests.post(url, headers=headers, json=payload)
    
    # Check if the response is successful (status code 201 Created)
    if response.status_code == 201:
        return None
    elif response.status_code in [200, 202]:
        return response.json()
    else:
        raise Exception(f"Failed to create issue. Status code: {response.status_code}, Response: {response.text}")