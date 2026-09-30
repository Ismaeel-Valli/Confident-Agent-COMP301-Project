import requests

def solve(inputs):
    """
    Lists commits for a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - page_size (int): The number of results per page (max 100).
            - credential (str): The caller-supplied credential (e.g., Bearer token or OAuth token).
    
    Returns:
        dict or None: The decoded JSON response if commits are found, or None for a successful empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    page_size = inputs["page_size"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential}",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    params = {
        "per_page": page_size
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to list commits. Status code: {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response (empty list of commits)
    if not data:
        return None
    
    return data