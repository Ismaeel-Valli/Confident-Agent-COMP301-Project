import requests

def solve(inputs):
    """
    Updates a milestone in a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - milestone_number (int): The number that identifies the milestone.
            - new_description (str): Value for the description attribute.
            - new_title (str): Value for the title attribute.
            - credential (dict): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, otherwise None.
    
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
        "X-GitHub-Api-Version": "2026-03-10"
    }

    # Prepare the payload for updating the milestone
    data = {
        "title": new_title,
        "description": new_description
    }

    response = requests.put(url, json=data, headers=headers, auth=credential)

    if response.status_code == 200:
        return None
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"Failed to update milestone. Status code: {response.status_code}, Response: {response.text}")