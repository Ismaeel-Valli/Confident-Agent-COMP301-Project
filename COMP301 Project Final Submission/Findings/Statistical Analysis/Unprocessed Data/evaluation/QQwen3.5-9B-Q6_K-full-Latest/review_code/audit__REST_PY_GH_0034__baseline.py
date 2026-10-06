import requests

def solve(inputs):
    """
    Updates a milestone in a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'repository_owner' (str): The account owner of the repository.
            - 'repository_name' (str): The name of the repository (without .git).
            - 'milestone_number' (int): The milestone number to update.
            - 'new_title' (str): The new title for the milestone.
            - 'credential' (dict): Contains authentication details, assumed to have necessary permissions.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, otherwise None.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs['repository_owner']
    repo = inputs['repository_name']
    milestone_number = inputs['milestone_number']
    new_title = inputs['new_title']
    credential = inputs['credential']
    
    # Construct the API URL for updating a milestone
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones/{milestone_number}"
    
    # Prepare headers with authentication
    headers = {
        'Authorization': f"token {credential.get('token', '')}",
        'Accept': 'application/vnd.github+json'
    }
    
    # Prepare the payload for updating the milestone title
    data = {
        "title": new_title
    }
    
    # Send the PUT request to update the milestone
    response = requests.put(url, headers=headers, json=data)
    
    # Check if the response is successful (2xx status code)
    if response.status_code >= 200 and response.status_code < 300:
        return response.json() if response.content else None
    
    # Raise an exception for unsuccessful HTTP responses
    raise Exception(f"Failed to update milestone. Status code: {response.status_code}, Response: {response.text}")