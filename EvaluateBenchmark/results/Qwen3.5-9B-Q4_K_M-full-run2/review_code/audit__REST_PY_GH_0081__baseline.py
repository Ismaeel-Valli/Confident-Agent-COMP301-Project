import requests

def solve(inputs):
    """
    Updates a label on a GitHub repository using the REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - name (str): The name of the label to update.
            - new_color (str): The new color value for the label.
            - credential (dict): Caller-supplied credential information (e.g., token).
    
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    repository_owner = inputs["repository_owner"]
    repository_name = inputs["repository_name"]
    name = inputs["name"]
    new_color = inputs["new_color"]
    credential = inputs["credential"]

    # Construct the API URL for updating a label
    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/labels/{name}"

    # Prepare headers with authentication
    headers = {
        "Authorization": f"token {credential.get('token', '')}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    # Prepare the payload for updating the label
    payload = {
        "color": new_color
    }

    # Send the PATCH request to update the label
    response = requests.patch(url, headers=headers, json=payload)

    # Check if the response is successful
    if response.status_code == 200:
        return None  # Successful empty response
    elif response.status_code == 204:
        return None  # No content response is also considered successful
    else:
        raise Exception(f"Failed to update label. Status code: {response.status_code}, Response: {response.text}")