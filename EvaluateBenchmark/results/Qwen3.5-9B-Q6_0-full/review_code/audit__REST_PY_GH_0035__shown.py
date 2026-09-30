import requests

def solve(inputs):
    """
    Delete a GitHub milestone using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Must contain:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Repository name without .git extension
            - milestone_number (int): Milestone number to delete
            - credential (str): Bearer token for authentication
    
    Returns:
        int: Successful HTTP status code (204)
    
    Raises:
        Exception: If the DELETE request fails or returns an unsuccessful status
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    milestone_number = inputs["milestone_number"]
    credential = inputs["credential"]
    
    # Construct the API URL for deleting a milestone
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones/{milestone_number}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.delete(url, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failed to delete milestone. Status code: {response.status_code}, Response: {response.text}")
    
    return response.status_code