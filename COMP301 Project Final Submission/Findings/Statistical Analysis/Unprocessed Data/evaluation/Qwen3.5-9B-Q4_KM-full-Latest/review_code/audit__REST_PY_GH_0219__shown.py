def solve(inputs):
    """
    List organization repositories using GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - organization (str): The organization name
            - type (str): Specifies the types of repositories to return
            - page_size (int): Number of results per page (max 100)
            - credential (str): Caller-supplied authentication token
    
    Returns:
        list or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    base_url = "https://api.github.com"
    org = inputs["organization"]
    repo_type = inputs["type"]
    page_size = min(inputs["page_size"], 100)
    auth_token = inputs["credential"]
    
    url = f"{base_url}/orgs/{org}/repos?per_page={page_size}&sort=updated&direction=desc"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {auth_token}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data