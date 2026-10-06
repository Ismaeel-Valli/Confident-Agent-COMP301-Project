import requests

def solve(inputs):
    """
    Updates a milestone in a GitHub repository using the REST API.
    
    Parameters:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - milestone_number (int): The number identifying the milestone.
            - new_description (str): New value for the description attribute.
            - new_title (str): New value for the title attribute.
            - credential (dict): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    milestone_number = inputs["milestone_number"]
    new_description = inputs["new_description"]
    new_title = inputs["new_title"]
    credential = inputs["credential"]

    # Construct the API URL for updating a milestone
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones/{milestone_number}"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential['token']}",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    data = {
        "title": new_title,
        "description": new_description
    }

    response = requests.patch(url, headers=headers, json=data)

    if response.status_code != 200:
        raise Exception(f"Failed to update milestone: HTTP {response.status_code}, Response: {response.text}")

    return response.json() if response.text else None