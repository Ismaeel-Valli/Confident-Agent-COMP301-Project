import requests

def solve(inputs):
    """
    List issue comments for a GitHub repository using the REST API v2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - issue_number (int): The issue number to fetch comments for.
            - page_size (int): Number of results per page (max 100).
            - credential (str): Bearer token for authentication.
    
    Returns:
        list or None: List of comment objects if comments exist, None if empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    issue_number = inputs["issue_number"]
    page_size = inputs["page_size"]
    credential = inputs["credential"]
    
    base_url = "https://api.github.com"
    url = f"{base_url}/repos/{owner}/{repo}/issues/{issue_number}/comments"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    params = {
        "per_page": page_size
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch issue comments. Status code: {response.status_code}")
    
    data = response.json()
    
    # Return None for empty successful response as per requirement
    return data if data else None