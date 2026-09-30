import requests

def solve(inputs):
    """
    List pull request files for a GitHub repository.
    
    Args:
        inputs (dict): Contains:
            - repository_owner: str, account owner of the repository
            - repository_name: str, name of the repository (without .git)
            - pull_number: int, pull request number
            - page_size: int, results per page (max 100)
            - page: int, page number to fetch
            - credential: str, caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    pr_number = inputs["pull_number"]
    page_size = inputs["page_size"]
    page = inputs["page"]
    credential = inputs["credential"]
    
    # GitHub REST API v2026-03-10 endpoint for pull request files
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {credential}"
    }
    
    params = {
        "page": page,
        "per_page": page_size
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data