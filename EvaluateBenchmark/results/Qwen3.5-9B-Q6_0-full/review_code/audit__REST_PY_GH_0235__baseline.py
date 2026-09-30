import requests

def solve(inputs):
    """
    Updates a pull request on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - pull_number (int): The number that identifies the pull request.
            - new_state (str): Value for the state attribute.
            - new_title (str): Value for the title attribute.
            - credential (dict): Caller-supplied credentials (assumed to have necessary permissions).
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, otherwise None.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    pull_number = inputs["pull_number"]
    new_state = inputs["new_state"]
    new_title = inputs["new_title"]
    credential = inputs["credential"]

    # Construct the API URL for updating a pull request
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}"

    # Prepare headers with authentication
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
        "Authorization": f"Bearer {credential['token']}"
    }

    # Prepare the payload for updating the pull request
    data = {
        "state": new_state,
        "title": new_title
    }

    try:
        response = requests.put(url, headers=headers, json=data)
        
        if response.status_code == 200 or response.status_code == 204:
            # GitHub often returns an empty body for successful updates (204 No Content)
            return None if response.status_code == 204 else response.json()
        else:
            raise Exception(f"Failed to update pull request. Status code: {response.status_code}, Response: {response.text}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"A network error occurred while updating the pull request: {str(e)}")