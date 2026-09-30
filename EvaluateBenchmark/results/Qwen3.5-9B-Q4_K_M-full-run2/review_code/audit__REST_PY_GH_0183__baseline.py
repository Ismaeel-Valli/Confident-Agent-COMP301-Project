import requests

def solve(inputs):
    """
    Updates a label on a GitHub repository using the REST API.
    
    Parameters:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - name (str): The current name of the label to update.
            - new_description (str): The new description for the label.
            - new_new_name (str): The new name for the label.
            - credential (dict): Caller-supplied credentials (e.g., token or auth headers).
    
    Returns:
        dict or None: Decoded JSON response if successful and non-empty, otherwise None.
    
    Raises:
        Exception: If the HTTP response indicates an error (non-2xx status code).
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    label_name = inputs["name"]
    new_description = inputs["new_description"]
    new_label_name = inputs["new_new_name"]
    credential = inputs["credential"]

    # Construct the API URL for updating a label
    url = f"https://api.github.com/repos/{owner}/{repo}/labels/{label_name}"

    # Prepare headers based on credential (assuming token in 'token' key or similar)
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {credential.get('token', '')}" if isinstance(credential, dict) else ""
    }

    # Prepare the payload for updating the label
    data = {
        "name": new_label_name,
        "description": new_description
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        return None  # Successful empty response
    elif response.status_code == 204:
        return None  # No content on success
    else:
        raise Exception(f"Failed to update label. Status code: {response.status_code}, Response: {response.text}")