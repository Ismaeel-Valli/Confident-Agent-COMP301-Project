import requests

def solve(inputs):
    """
    Updates a milestone in a GitHub repository using the REST API.
    
    Parameters:
        inputs (dict): A dictionary containing:
            - 'repository_owner' (str): The account owner of the repository.
            - 'repository_name' (str): The name of the repository (without .git).
            - 'milestone_number' (int): The milestone number to update.
            - 'new_title' (str): The new title for the milestone.
            - 'credential' (dict): Contains authentication details, assumed to have necessary permissions.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty; None if the response is empty.
    
    Raises:
        Exception: If the HTTP response indicates an error (status code >= 400).
    """
    repository_owner = inputs['repository_owner']
    repository_name = inputs['repository_name']
    milestone_number = inputs['milestone_number']
    new_title = inputs['new_title']
    credential = inputs['credential']

    # Construct the API URL for updating a milestone
    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/milestones/{milestone_number}"

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {credential.get('token', '')}" if credential.get('token') else ""
    }

    # Prepare the payload for updating the milestone
    data = {
        "title": new_title
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code >= 400:
        raise Exception(f"Failed to update milestone. Status code: {response.status_code}, Response: {response.text}")

    return response.json() if response.text else None