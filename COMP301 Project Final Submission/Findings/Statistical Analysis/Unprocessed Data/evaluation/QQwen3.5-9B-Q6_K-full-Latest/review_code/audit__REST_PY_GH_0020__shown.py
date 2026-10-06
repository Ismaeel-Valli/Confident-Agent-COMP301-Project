import requests

def solve(inputs):
    """Delete a GitHub issue comment using the REST API v2026-03-10."""
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    comment_id = inputs["comment_id"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/comments/{comment_id}"
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    
    return response.status_code