import requests
from urllib.parse import quote

def solve(inputs):
    """
    Updates a label in a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - name (str): The current name of the label to update.
            - new_description (str): The new description for the label.
            - new_new_name (str): The new name for the label.
            - credential (dict): Caller-supplied credentials (assumed to have necessary permissions).
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, otherwise None.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    current_name = inputs["name"]
    new_description = inputs["new_description"]
    new_name = inputs["new_new_name"]
    credential = inputs["credential"]

    # Construct the URL for updating a label
    url = f"https://api.github.com/repos/{owner}/{repo}/labels/{quote(current_name)}"

    # Prepare headers with authentication
    headers = {
        "Authorization": f"token {credential.get('token', '')}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
        "Content-Type": "application/json"
    }

    # Prepare the payload for updating the label
    payload = {
        "name": new_name,
        "description": new_description
    }

    try:
        response = requests.put(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            # Return None for a successful empty response
            return None
        elif response.status_code == 201:
            # If the label was created (shouldn't happen in an update, but handled for completeness)
            return response.json()
        else:
            raise Exception(f"Failed to update label. Status code: {response.status_code}, Response: {response.text}")
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"A request error occurred: {str(e)}")