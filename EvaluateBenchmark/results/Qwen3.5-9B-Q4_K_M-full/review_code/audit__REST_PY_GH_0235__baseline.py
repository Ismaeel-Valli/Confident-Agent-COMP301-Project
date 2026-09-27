import requests

def solve(inputs):
    """
    Updates a pull request in a GitHub repository using the REST API.
    
    Parameters:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - pull_number (int): The number identifying the pull request.
            - new_state (str): The new state for the pull request ('open', 'closed', or 'merged').
            - new_title (str): The new title for the pull request.
            - credential (dict): Caller-supplied credentials (e.g., token in 'token' key).
    
    Returns:
        dict or None: Decoded JSON response if successful, None for an empty success response.
    
    Raises:
        Exception: If the HTTP response indicates failure (non-2xx status code).
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    pr_number = inputs["pull_number"]
    new_state = inputs["new_state"]
    new_title = inputs["new_title"]
    credential = inputs["credential"]

    # Construct the API URL for updating a pull request (GitHub v2026-03-10)
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {credential.get('token', '')}"
    }

    payload = {
        "state": new_state,
        "title": new_title
    }

    response = requests.put(url, json=payload, headers=headers)

    if response.status_code == 200:
        return None  # Successful empty response
    elif response.status_code == 201:
        return response.json()  # Created (though PUT usually returns 200 or 204)
    else:
        raise Exception(f"Failed to update pull request. Status code: {response.status_code}, Response: {response.text}")