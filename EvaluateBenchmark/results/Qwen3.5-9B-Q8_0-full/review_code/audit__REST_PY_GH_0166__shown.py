import requests

def solve(inputs):
    """
    Fetch repository tags from GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Must contain:
            - repository_owner (str)
            - repository_name (str)
            - page_size (int, max 100)
            - page (int)
            - credential (str)
    
    Returns:
        list or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    page_size = inputs["page_size"]
    page = inputs["page"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/tags"
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    params = {
        "per_page": page_size,
        "page": page
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data