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
    base_url = "https://api.github.com"
    endpoint = f"/orgs/{org}/repos"
    
    # Build query parameters based on type
    params = {}
    if repo_type:
        params["type"] = repo_type
    
    # Prepare headers with authentication
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    url = base_url + endpoint
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        # Raise exception for unsuccessful HTTP responses (4xx, 5xx)
        response.raise_for_status()
        
        # Check if response is empty
        if not response.text.strip():
            return None
        
        # Decode and return JSON response
        data = response.json()
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"GitHub API request failed: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request error occurred: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to decode JSON response: {e}")