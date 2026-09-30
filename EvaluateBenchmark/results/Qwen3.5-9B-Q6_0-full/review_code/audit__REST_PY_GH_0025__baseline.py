import requests
import json

def solve(inputs):
    """
    Lists labels for a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'repository_owner' (str): The account owner of the repository.
            - 'repository_name' (str): The name of the repository (without .git).
            - 'credential' (str): The authentication token or Bearer token for the API call.
    
    Returns:
        list | None: A list of label dictionaries if labels exist, otherwise None for an empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx range).
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/labels"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential}",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response (no labels)
    if not data:
        return None
    
    return data