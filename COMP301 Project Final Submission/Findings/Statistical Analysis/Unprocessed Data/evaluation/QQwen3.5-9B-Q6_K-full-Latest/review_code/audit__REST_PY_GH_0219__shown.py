import requests

def solve(inputs):
    """
    List organization repositories from GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - organization (str): Organization name
            - type (str): Repository types to filter by
            - page_size (int): Results per page (max 100)
            - credential (str): Bearer token for authentication
    
    Returns:
        list or None: Decoded JSON response, or None if empty
    """
    org = inputs["organization"]
    repo_type = inputs["type"]
    page_size = inputs["page_size"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/orgs/{org}/repos"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github.v2026-03-10+json"
    }
    
    params = {
        "type": repo_type,
        "per_page": page_size
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}")
    
    data = response.json()
    
    return data if data else None