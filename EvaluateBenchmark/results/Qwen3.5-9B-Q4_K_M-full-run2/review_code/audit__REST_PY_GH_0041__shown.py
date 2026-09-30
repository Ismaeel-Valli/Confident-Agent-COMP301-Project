import requests
import json

def solve(inputs):
    """
    List pull request files for a GitHub repository.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - pull_number (int): Pull request number
            - credential (str): Caller-supplied authentication token
    
    Returns:
        list or None: List of files in the pull request, or None if empty
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    pr_number = inputs["pull_number"]
    credential = inputs["credential"]
    
    # Construct the API URL for GitHub REST API v2026-03-10
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    
    # Prepare headers with Bearer token authentication
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Make the GET request
    response = requests.get(url, headers=headers)
    
    # Check for unsuccessful HTTP response
    if response.status_code != 200:
        raise Exception(f"GitHub API returned status code {response.status_code}: {response.text}")
    
    # Decode and return the JSON response
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data