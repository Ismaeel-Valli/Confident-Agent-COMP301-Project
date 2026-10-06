import requests

def solve(inputs):
    """
    Updates a pull request on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - pull_number (int): The number that identifies the pull request.
            - new_state (str): The new state for the pull request ('open' or 'closed').
            - new_title (str): The new title for the pull request.
            - credential (dict): Contains authentication details, assumed to have necessary permissions.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, otherwise None.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    # Construct the URL for updating a pull request
    url = f"https://api.github.com/repos/{inputs['repository_owner']}/{inputs['repository_name']}/pulls/{inputs['pull_number']}"
    
    # Prepare the headers with authentication
    headers = {
        "Authorization": f"token {inputs['credential']['token']}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Prepare the payload for updating the pull request
    payload = {
        "state": inputs['new_state'],
        "title": inputs['new_title']
    }
    
    # Send the PUT request to update the pull request
    response = requests.put(url, headers=headers, json=payload)
    
    # Check if the response is successful
    if response.status_code == 200:
        # Return None for a successful empty response
        return None if not response.text else response.json()
    elif response.status_code == 404:
        raise Exception(f"Resource not found: {response.url}")
    elif response.status_code == 403:
        raise Exception("Forbidden: Insufficient permissions or invalid credentials.")
    else:
        # Raise an exception for any other unsuccessful HTTP response
        raise Exception(f"Failed to update pull request. Status code: {response.status_code}, Response: {response.text}")