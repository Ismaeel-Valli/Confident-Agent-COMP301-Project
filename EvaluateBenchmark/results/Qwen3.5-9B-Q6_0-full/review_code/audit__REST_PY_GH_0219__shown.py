import requests

def solve(inputs):
    """
    List organization repositories from GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - organization (str): The organization name
            - type (str): Repository types to filter by
            - page_size (int): Number of results per page (max 100)
            - credential (str): Authentication token
    
    Returns:
        list or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    org = inputs["organization"]
    repo_type = inputs["type"]
    page_size = inputs["page_size"]
    credential = inputs["credential"]
    
    base_url = "https://api.github.com"
    endpoint = f"/orgs/{org}/repos"
    url = f"{base_url}{endpoint}"
    
    params = {
        "type": repo_type,
        "per_page": page_size
    }
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data