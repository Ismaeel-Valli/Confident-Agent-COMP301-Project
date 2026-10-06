import requests
import json

def solve(inputs):
    """
    Creates a new issue in a GitHub repository using the REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - new_assignees (list): List of assignee usernames or URLs.
            - new_body (str): The body text of the issue.
            - new_labels (list): List of label names or URLs.
            - new_title (str): The title of the issue.
            - credential (dict): Caller-supplied credentials (e.g., token in 'token' key).
    
    Returns:
        dict: Decoded JSON response from GitHub API.
              Returns None if the response body is empty on success.
    
    Raises:
        Exception: If the HTTP response indicates an error (non-2xx status code).
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    assignees = inputs["new_assignees"]
    body = inputs["new_body"]
    labels = inputs["new_labels"]
    title = inputs["new_title"]
    credential = inputs["credential"]

    # Construct the API URL for creating an issue
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    # Prepare headers with authentication
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {credential.get('token', '')}"
    }

    # Prepare the payload for the issue creation
    data = {
        "title": title,
        "body": body,
        "assignees": assignees,
        "labels": labels
    }

    # Send POST request to create the issue
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful (status code 201 Created or similar success codes)
    if response.status_code == 201:
        return response.json() if response.text else None
    elif response.status_code == 422:
        # Validation error, but we still raise an exception as per instructions
        pass

    # Raise an exception for any unsuccessful HTTP response
    response.raise_for_status()