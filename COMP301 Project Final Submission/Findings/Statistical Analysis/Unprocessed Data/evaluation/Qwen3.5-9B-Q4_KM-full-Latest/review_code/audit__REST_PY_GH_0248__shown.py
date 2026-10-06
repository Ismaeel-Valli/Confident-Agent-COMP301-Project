import requests

def solve(inputs):
    """
    List repository issues for GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git extension)
            - since (str): ISO 8601 timestamp for filtering issues updated after this time
            - credential (str): Bearer token for authentication
    
    Returns:
        list or None: Decoded JSON response as a list, or None if empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses (non-2xx status codes)
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    since = inputs["since"]
    credential = inputs["credential"]
    
    url = "https://api.github.com/repos/{owner}/{repo}/issues".format(owner=owner, repo=repo)
    params = {"since": since}
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data