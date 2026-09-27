import requests
import json

def solve(inputs):
    """
    Updates a milestone in a GitHub repository using the REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - milestone_number (int): The number that identifies the milestone.
            - new_description (str): New value for the description attribute.
            - new_title (str): New value for the title attribute.
            - credential (dict): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    repository_owner = inputs["repository_owner"]
    repository_name = inputs["repository_name"]
    milestone_number = inputs["milestone_number"]
    new_description = inputs["new_description"]
    new_title = inputs["new_title"]
    credential = inputs["credential"]

    # Construct the API URL for updating a milestone
    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/milestones/{milestone_number}"

    # Prepare headers with authentication
    headers = {
        "Authorization": f"token {credential.get('token', '')}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    # Prepare the payload for updating the milestone
    payload = {
        "title": new_title,
        "description": new_description
    }

    # Send PATCH request to update the milestone
    response = requests.patch(url, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        return None  # Successful empty response
    elif response.status_code == 204:
        return None  # No content returned for successful update
    else:
        raise Exception(f"Failed to update milestone. Status code: {response.status_code}, Response: {response.text}")