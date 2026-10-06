import requests

def solve(inputs):
    """
    Fetch pull request files from GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Must contain:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Repository name without .git extension
            - pull_number (int): Pull request number
            - page_size (int): Results per page (max 100)
            - page (int): Page number to fetch
            - credential (str): Bearer token for authentication
    
    Returns:
        list or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    pr_number = inputs["pull_number"]
    page_size = inputs["page_size"]
    page = inputs["page"]
    credential = inputs["credential"]
    
    # GitHub API v2026-03-10 endpoint for pull request files
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    params = {
        "page": page,
        "per_page": page_size
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data