import requests

def solve(inputs):
    """
    Fetch issue comments from GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains repository_owner, repository_name, issue_number,
                       since, page, and credential.
    
    Returns:
        list or None: Decoded JSON response, or None for empty successful response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    issue_number = inputs["issue_number"]
    since = inputs.get("since")
    page = inputs.get("page", 1)
    credential = inputs["credential"]
    
    base_url = "https://api.github.com"
    url = f"{base_url}/repos/{owner}/{repo}/issues/{issue_number}/comments"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {credential}"
    }
    
    params = {"page": page}
    if since:
        params["since"] = since
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data