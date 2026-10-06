import requests

def solve(inputs):
    """
    List commits from a GitHub repository that contain changes to a specific file path.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): The account owner of the repository
            - repository_name (str): The name of the repository without .git extension
            - path (str): File path to filter commits by
            - credential (str): GitHub API token or authentication string
    
    Returns:
        list or None: List of commit objects if commits found, None for empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    file_path = inputs["path"]
    token = inputs["credential"]
    
    # GitHub API v3 endpoint for listing commits with a specific path filter
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    params = {
        "path": file_path,
        "per_page": 100  # GitHub default is 30, but we'll use a reasonable number
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data