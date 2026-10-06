import requests

def solve(inputs):
    """
    List organization repositories from GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - organization (str): The organization name
            - sort (str): The property to sort the results by
            - credential (str): Bearer token for authentication
    
    Returns:
        list or None: Decoded JSON response, or None if empty
    """
    org = inputs["organization"]
    sort_by = inputs["sort"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/orgs/{org}/repos"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}")
    
    data = response.json()
    
    if len(data) == 0:
        return None
    
    return data