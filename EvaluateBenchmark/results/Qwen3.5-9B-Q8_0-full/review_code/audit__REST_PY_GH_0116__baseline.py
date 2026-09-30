import requests
from urllib.parse import quote

def solve(inputs):
    """
    Creates a label in a GitHub repository using the REST API version 2026-03-10.
    
    Note: The function signature and description in the prompt mention creating a 'label', 
    but the input parameters (new_description, new_name) are typically used for updating 
    an issue or pull request, not creating a label. GitHub labels are created with a name, 
    color, and description. However, based on the inputs provided (repository_owner, repository_name, 
    new_description, new_name), this function will attempt to create a label with the given name 
    and description.
    
    Parameters:
    inputs (dict): A dictionary containing:
        - repository_owner (str): The account owner of the repository
        - repository_name (str): The name of the repository without the .git extension
        - new_description (str): Value for the description attribute
        - new_name (str): Value for the name attribute
        - credential (str): Caller-supplied credential (token)
    
    Returns:
    dict or None: Decoded JSON response. Returns None for a successful empty response.
    
    Raises:
    Exception: For an unsuccessful HTTP response.
    """
    
    repository_owner = inputs["repository_owner"]
    repository_name = inputs["repository_name"]
    new_description = inputs["new_description"]
    new_name = inputs["new_name"]
    credential = inputs["credential"]
    
    # Construct the API URL for creating a label
    url = f"https://api.github.com/repos/{quote(repository_owner, safe='')}/{quote(repository_name, safe='')}/labels"
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    data = {
        "name": new_name,
        "description": new_description
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        # Successful creation, but the response might be empty or contain the created label
        return response.json() if response.content else None
    elif response.status_code in [400, 403, 404, 422]:
        raise Exception(f"Failed to create label: {response.status_code} - {response.text}")
    else:
        raise Exception(f"Unexpected error: {response.status_code} - {response.text}")