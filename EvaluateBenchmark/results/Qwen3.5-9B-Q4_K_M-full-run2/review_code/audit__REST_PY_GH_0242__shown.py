import requests

def solve(inputs):
    """
    List organization repositories from GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - organization (str): The organization name
            - type (str): The types of repositories to return
            - page (int): The page number of results to fetch
            - credential (str): Caller-supplied authentication token
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.github.com"
    org = inputs["organization"]
    repo_type = inputs["type"]
    page = inputs["page"]
    credential = inputs["credential"]
    
    url = f"{base_url}/orgs/{org}/repos?per_page=100&page={page}&type={repo_type}"
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    return data if data else None