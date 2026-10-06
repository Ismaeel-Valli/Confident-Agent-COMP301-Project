import requests

def solve(inputs):
    """
    List commits from a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - page_size (int): The number of results per page (max 100).
            - credential (str): The caller-supplied credential (e.g., token or Bearer token).
    
    Returns:
        list or None: A list of commit objects if commits are found, otherwise None for an empty response.
        Raises:
            requests.RequestException: If the HTTP request fails.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    page_size = inputs["page_size"]
    credential = inputs["credential"]
    
    # GitHub API version 2026-03-10 endpoint for listing commits
    base_url = "https://api.github.com"
    url = f"{base_url}/repos/{owner}/{repo}/commits"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential}"
    }
    
    params = {
        "per_page": page_size
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise requests.RequestException(f"Failed to fetch commits. Status code: {response.status_code}")
    
    data = response.json()
    
    # Return None for an empty list of commits
    if not data:
        return None
    
    return data