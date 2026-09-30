import requests


def solve(inputs):
    """
    List milestones for a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git extension).
            - page (int): The page number of results to fetch.
            - credential (str): The caller-supplied authentication token.
    
    Returns:
        list or None: A list of milestone objects from the API response, or None if empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx).
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    page = inputs["page"]
    credential = inputs["credential"]
    
    # GitHub API v2026-03-10 endpoint for listing milestones
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones?page={page}"
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (empty list)
    if not data:
        return None
    
    return data