import requests

def solve(inputs):
    """
    List commits for a GitHub repository containing a specific file path.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - path (str): File path to filter commits by
            - credential (str): Bearer token for authentication
    
    Returns:
        list or None: Decoded JSON response, or None if empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    file_path = inputs["path"]
    token = inputs["credential"]
    
    url = "https://api.github.com/repos/{owner}/{repo}/commits".format(owner=owner, repo=repo)
    params = {"path": file_path}
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
    
    return data