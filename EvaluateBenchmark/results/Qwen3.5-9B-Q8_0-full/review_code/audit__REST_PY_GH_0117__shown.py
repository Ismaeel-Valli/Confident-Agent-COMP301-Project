import requests

def solve(inputs):
    """
    Update a label on a GitHub repository.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - name (str): Label name to update
            - new_description (str): New description for the label
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    label_name = inputs["name"]
    new_description = inputs["new_description"]
    credential = inputs["credential"]
    
    # GitHub API v3 endpoint for updating a label
    url = f"https://api.github.com/repos/{owner}/{repo}/labels/{label_name}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Update the label description using PATCH method
    payload = {
        "description": new_description
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to update label: {response.status_code} - {response.text}")
    
    # Return decoded JSON response
    return response.json() if response.content else None