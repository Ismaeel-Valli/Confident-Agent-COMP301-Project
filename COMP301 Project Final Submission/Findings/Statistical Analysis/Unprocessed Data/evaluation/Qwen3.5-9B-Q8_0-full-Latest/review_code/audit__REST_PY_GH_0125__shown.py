import requests

def solve(inputs):
    """
    Fetch pull request files from GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Must contain:
            - repository_owner (str)
            - repository_name (str)
            - pull_number (int)
            - page (int)
            - credential (str)
    
    Returns:
        list or None: Decoded JSON response. Returns None for empty successful response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    pr_number = inputs["pull_number"]
    page = inputs["page"]
    credential = inputs["credential"]
    
    base_url = "https://api.github.com"
    url = f"{base_url}/repos/{owner}/{repo}/pulls/{pr_number}/files?page={page}"
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v2026-03-10+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data