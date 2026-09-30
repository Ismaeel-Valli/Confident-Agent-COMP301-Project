import requests

def solve(inputs):
    """
    Updates a GitHub issue using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository.
            - issue_number (int): The number that identifies the issue.
            - new_labels (list or None): New labels to set for the issue.
            - new_title (str): New title for the issue.
            - credential (str): Bearer token for authentication.
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    issue_number = inputs["issue_number"]
    new_labels = inputs.get("new_labels")
    new_title = inputs.get("new_title")
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json"
    }
    
    payload = {}
    if new_title is not None:
        payload["title"] = new_title
    if new_labels is not None:
        payload["labels"] = new_labels
    
    response = requests.put(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update issue. Status code: {response.status_code}, Response: {response.text}")
    
    return response.json() if response.content else None