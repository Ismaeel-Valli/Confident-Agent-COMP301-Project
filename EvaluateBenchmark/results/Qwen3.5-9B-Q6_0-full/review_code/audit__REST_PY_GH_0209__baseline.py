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
            - credential (dict): Caller-supplied credentials with 'token' key.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, otherwise None.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    repository_owner = inputs["repository_owner"]
    repository_name = inputs["repository_name"]
    milestone_number = inputs["milestone_number"]
    new_description = inputs["new_description"]
    new_title = inputs["new_title"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/milestones/{milestone_number}"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential['token']}",
        "X-GitHub-Api-Version": "2026-03-10",
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": new_title,
        "description": new_description
    }
    
    response = requests.put(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update milestone. Status code: {response.status_code}, Response: {response.text}")
    
    return response.json() if response.content else None