import requests

def solve(inputs):
    """
    Updates a milestone in a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - milestone_number (int): The number that identifies the milestone.
            - new_title (str): The new value for the title attribute.
            - credential (str): The authentication token or string for API access.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, otherwise None.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    milestone_number = inputs["milestone_number"]
    new_title = inputs["new_title"]
    credential = inputs["credential"]

    url = f"https://api.github.com/repos/{owner}/{repo}/milestones/{milestone_number}"
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    data = {
        "title": new_title
    }

    response = requests.put(url, json=data, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update milestone. Status code: {response.status_code}, Response: {response.text}")
    
    return response.json() if response.text else None