import requests

def solve(inputs):
    """
    List releases from GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git extension)
            - page_size (int): Number of results per page (max 100)
            - page (int): Page number of results to fetch
            - credential (str): Caller-supplied authentication token
    
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
    
    # GitHub API v3 endpoint for releases
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential}"
    }
    
    params = {
        "per_page": page_size,
        "page": page
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch releases: HTTP {response.status_code}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data