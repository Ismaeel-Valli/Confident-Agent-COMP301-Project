import requests

def solve(inputs):
    """
    List commits on a GitHub pull request using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - pull_number (int): Pull request number
            - page_size (int): Number of results per page (max 100)
            - credential (str): Caller-supplied authentication token
    
    Returns:
        list or None: Decoded JSON response as a list of commits, or None if empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses (non-2xx status codes).
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    pr_num = inputs["pull_number"]
    page_size = min(inputs.get("page_size", 30), 100)
    token = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_num}/commits"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    params = {"per_page": page_size}
    
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    
    data = resp.json()
    return data if data else None