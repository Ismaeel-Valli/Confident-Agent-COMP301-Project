import requests
import json


def solve(inputs):
    """
    List pull request files for a given GitHub repository and PR number.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): The account owner of the repository
            - repository_name (str): The name of the repository without .git extension
            - pull_number (int): The number that identifies the pull request
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    pr_number = inputs["pull_number"]
    credential = inputs["credential"]
    
    # GitHub API v3 endpoint for listing files in a pull request
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (no files changed)
    if not data:
        return None
    
    return data