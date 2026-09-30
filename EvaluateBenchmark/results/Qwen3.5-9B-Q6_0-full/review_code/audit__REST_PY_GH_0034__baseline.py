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
    
    # Construct the URL for updating a milestone
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones/{milestone_number}"
    
    # Prepare headers with authentication
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2026-03-10'
    }
    
    # Add authorization if provided (assuming token in credential)
    if 'token' in credential:
        headers['Authorization'] = f"Bearer {credential['token']}"
    
    # Prepare the payload for updating the milestone
    data = {
        "title": new_title
    }
    
    # Send the PUT request to update the milestone
    response = requests.put(url, json=data, headers=headers)
    
    # Check if the response is successful
    if response.status_code == 200:
        return None  # Successful empty response
    elif response.status_code == 204:
        return None  # No content response
    else:
        raise Exception(f"Failed to update milestone. Status code: {response.status_code}, Response: {response.text}")