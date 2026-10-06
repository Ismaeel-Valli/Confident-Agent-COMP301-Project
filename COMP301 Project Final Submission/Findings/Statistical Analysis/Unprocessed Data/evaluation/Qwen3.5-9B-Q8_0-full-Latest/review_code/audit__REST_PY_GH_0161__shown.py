import requests

def solve(inputs):
    """
    Fetch releases from GitHub REST API v2026-03-10.
    
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
    
    base_url = "https://api.github.com"
    url = f"{base_url}/repos/{owner}/{repo}/releases"
    
    params = {
        "per_page": page_size,
        "page": page
    }
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API returned status code {response.status_code}")
    
    data = response.json()
    
    if len(data) == 0:
        return None
    
    return data