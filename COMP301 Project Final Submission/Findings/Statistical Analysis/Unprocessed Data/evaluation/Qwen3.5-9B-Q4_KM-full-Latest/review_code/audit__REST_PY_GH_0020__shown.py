import requests

def solve(inputs):
    """
    Delete a GitHub issue comment using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository.
            - repository_name (str): Name of the repository (without .git).
            - comment_id (int): Unique identifier of the comment to delete.
            - credential (str): Caller-supplied authentication token.
    
    Returns:
        int: HTTP status code of the successful deletion response (204).
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful deletion.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    comment_id = inputs["comment_id"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/comments/{comment_id}"
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json"
    }
    
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    
    return response.status_code