def solve(inputs):
    """
    Delete an issue comment on GitHub using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository.
            - repository_name (str): Name of the repository (without .git).
            - comment_id (int): Unique identifier of the comment to delete.
            - credential (str): Caller-supplied authentication token.
    
    Returns:
        int: HTTP status code 204 on success.
    
    Raises:
        Exception: If the HTTP response indicates failure.
    """
    import requests
    
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    comment_id = inputs["comment_id"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/comments/{comment_id}"
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    
    return response.status_code