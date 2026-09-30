import requests
from urllib.parse import quote

def solve(inputs):
    """
    Lists repository issues for GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - since (str): ISO 8601 timestamp to filter issues updated after this time.
            - credential (str): Bearer token for authentication.
    
    Returns:
        list or None: Decoded JSON response as a list, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response status code indicates an error.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    since = inputs["since"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {}
    if since:
        params["since"] = since
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    return data if data else None