import requests
import json

def solve(inputs):
    """
    Creates a pull request on GitHub using the REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - new_base (str): Value for the base attribute.
            - new_body (str): Value for the body attribute.
            - new_draft (bool): Value for the draft attribute.
            - new_head (str): Value for the head attribute.
            - new_title (str): Value for the title attribute.
            - credential (dict): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: The decoded JSON response if successful, None for an empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    repository_owner = inputs["repository_owner"]
    repository_name = inputs["repository_name"]
    new_base = inputs["new_base"]
    new_body = inputs["new_body"]
    new_draft = inputs["new_draft"]
    new_head = inputs["new_head"]
    new_title = inputs["new_title"]
    credential = inputs["credential"]

    # Construct the API URL for creating a pull request
    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/pulls"

    # Prepare the payload
    payload = {
        "title": new_title,
        "body": new_body,
        "head": new_head,
        "base": new_base,
        "draft": new_draft
    }

    # Prepare headers with authentication
    headers = {
        "Authorization": f"token {credential.get('token', '')}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    # Send the POST request to create the pull request
    response = requests.post(url, json=payload, headers=headers)

    # Check if the response is successful
    if response.status_code == 201:
        return None  # Successful empty response
    elif response.status_code == 422:
        # Validation error or other client-side issue
        raise Exception(f"Validation Error: {response.text}")
    else:
        # Unsuccessful HTTP response
        raise Exception(f"HTTP Error {response.status_code}: {response.text}")

    return None