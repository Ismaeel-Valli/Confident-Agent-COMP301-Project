import requests

def solve(inputs):
    """
    Updates a milestone in a GitHub repository using the REST API.
    
    Parameters:
        inputs (dict): A dictionary containing:
            - 'repository_owner': str, the account owner of the repository.
            - 'repository_name': str, the name of the repository (without .git).
            - 'milestone_number': int, the milestone number to update.
            - 'new_title': str, the new title for the milestone.
            - 'credential': dict, containing authentication details (e.g., token in 'token' key).
    
    Returns:
        None if the response is empty (success), otherwise returns the decoded JSON response.
    
    Raises:
        Exception: If the HTTP response indicates an error (non-2xx status code).
    """
    
    owner = inputs['repository_owner']
    repo = inputs['repository_name']
    milestone_number = inputs['milestone_number']
    new_title = inputs['new_title']
    credential = inputs['credential']
    
    # Construct the API URL for updating a milestone
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones/{milestone_number}"
    
    headers = {
        "Accept": "application/vnd.github+json"
    }
    
    # Prepare authentication based on common GitHub credential patterns
    if 'token' in credential:
        auth_header = f"Bearer {credential['token']}"
    elif 'username' in credential and 'password' in credential:
        auth_header = None  # Will use basic auth below if needed, but token is preferred
    else:
        raise ValueError("Credential must contain either a 'token' or both 'username' and 'password'.")
    
    if auth_header:
        headers["Authorization"] = auth_header
    
    # Prepare the payload for updating the milestone title
    data = {
        "title": new_title
    }
    
    response = requests.put(url, json=data, headers=headers)
    
    # Check for successful HTTP status code (2xx)
    if 200 <= response.status_code < 300:
        return None if response.text.strip() == "" else response.json()
    else:
        raise Exception(f"Failed to update milestone. Status code: {response.status_code}, Response: {response.text}")