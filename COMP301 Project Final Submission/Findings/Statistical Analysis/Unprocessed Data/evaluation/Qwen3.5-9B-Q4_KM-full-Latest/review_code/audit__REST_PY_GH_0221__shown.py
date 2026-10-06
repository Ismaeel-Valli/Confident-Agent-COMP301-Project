import requests

def solve(inputs):
    """
    Update a GitHub repository's wiki setting using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Repository name without .git extension
            - new_has_wiki (bool): New value for has_wiki attribute
            - credential (str): Bearer token for authentication
    
    Returns:
        None if successful with empty response, otherwise decoded JSON response.
    
    Raises:
        Exception for unsuccessful HTTP responses.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    has_wiki = inputs["new_has_wiki"]
    token = inputs["credential"]
    
    url = "https://api.github.com/repos/{owner}/{repo}".format(owner=owner, repo=repo)
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {"has_wiki": has_wiki}
    
    response = requests.patch(url, json=payload, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    return response.json()