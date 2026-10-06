import requests
import json

def solve(inputs):
    """
    Create a repository for the authenticated user on GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - new_name (str): Name for the new repository
            - credential (str): Authentication token
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    # GitHub API endpoint for creating a repository
    url = "https://api.github.com/user/repos"
    
    # Prepare headers with authentication
    headers = {
        "Authorization": f"token {inputs['credential']}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Prepare request payload
    payload = {
        "name": inputs["new_name"]
    }
    
    # Make the POST request to create repository
    response = requests.post(url, headers=headers, json=payload)
    
    # Check HTTP status code
    if response.status_code == 201:
        # Successful creation with empty body (GitHub returns empty JSON object)
        return None
    elif response.status_code == 200:
        # Also successful, return decoded JSON
        return response.json()
    else:
        # Unsuccessful response - raise exception
        raise Exception(f"Failed to create repository. Status code: {response.status_code}, Response: {response.text}")