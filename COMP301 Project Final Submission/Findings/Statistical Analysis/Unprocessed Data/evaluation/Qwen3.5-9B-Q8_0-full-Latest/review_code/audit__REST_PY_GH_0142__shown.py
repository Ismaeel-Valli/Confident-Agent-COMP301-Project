import requests
import json

def solve(inputs):
    """
    List commits from a GitHub repository filtered by author.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - author (str): GitHub username or email to filter commits
            - credential (str): Bearer token for authentication
    
    Returns:
        list: Decoded JSON response, or None if empty
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    author = inputs["author"]
    credential = inputs["credential"]
    
    # GitHub REST API v2026-03-10 endpoint for listing commits
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    params = {
        "author": author
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data