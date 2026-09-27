import requests

def solve(inputs):
    """
    List commits on a GitHub pull request using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - pull_number (int): Pull request number
            - page_size (int): Number of results per page (max 100)
            - page (int): Page number to fetch
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    pr_num = inputs["pull_number"]
    page_size = inputs["page_size"]
    page = inputs["page"]
    credential = inputs["credential"]
    
    # Construct the API URL for GitHub REST API v2026-03-10
    url = "https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/commits".format(
        owner=owner,
        repo=repo,
        pr_number=pr_num
    )
    
    # Prepare headers with Bearer token authentication
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Build query parameters
    params = {
        "page": page,
        "per_page": page_size
    }
    
    # Make the API request
    response = requests.get(url, headers=headers, params=params)
    
    # Raise exception for unsuccessful HTTP responses
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    # Decode and return the JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data