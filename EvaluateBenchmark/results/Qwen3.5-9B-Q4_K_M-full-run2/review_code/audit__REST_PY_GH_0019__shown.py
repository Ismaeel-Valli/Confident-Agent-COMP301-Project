import requests

def solve(inputs):
    """
    Update an issue comment on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository
            - comment_id (int): Unique identifier of the comment
            - new_body (str): New body content for the comment
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    comment_id = inputs["comment_id"]
    new_body = inputs["new_body"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/comments/{comment_id}"
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    response = requests.patch(url, json={"body": new_body}, headers=headers)
    
    if response.status_code not in [200, 204]:
        raise Exception(f"Failed to update comment: {response.status_code} - {response.text}")
    
    return response.json() if response.status_code == 200 else None