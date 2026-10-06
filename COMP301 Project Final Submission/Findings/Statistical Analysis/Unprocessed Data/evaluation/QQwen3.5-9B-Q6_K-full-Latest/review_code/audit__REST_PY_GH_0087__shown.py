import requests

def solve(inputs):
    """
    Update a pull request on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - pull_number (int): Pull request number
            - new_body (str): New body content for the PR
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    # Build the API URL for updating a pull request
    base_url = "https://api.github.com"
    url = f"{base_url}/repos/{inputs['repository_owner']}/{inputs['repository_name']}/pulls/{inputs['pull_number']}"
    
    # Prepare headers with authentication
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Prepare the payload
    payload = {
        "body": inputs['new_body']
    }
    
    # Make the PATCH request to update the pull request
    response = requests.patch(url, json=payload, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Return None for successful empty response, otherwise return decoded JSON
    if response.status_code == 204:
        return None
    
    return response.json()