import requests
import json

def solve(inputs):
    """
    List organization repositories from GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - organization (str): The organization name
            - type (str): Specifies the types of repositories to return
            - credential (str): Caller-supplied authentication token
    
    Returns:
        list or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    org = inputs["organization"]
    repo_type = inputs["type"]
    credential = inputs["credential"]
    
    # GitHub API endpoint for listing organization repositories
    url = f"https://api.github.com/orgs/{org}/repos"
    
    # Prepare headers with authentication
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response, otherwise return the list
    if len(data) == 0:
        return None
    
    return data