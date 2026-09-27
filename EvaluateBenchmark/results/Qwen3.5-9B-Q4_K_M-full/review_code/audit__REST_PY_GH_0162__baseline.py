import requests
import json

def solve(inputs):
    """
    Creates a release on GitHub using the REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - new_body (str): Value for the body attribute of the release.
            - new_tag_name (str): Value for the tag name attribute.
            - credential (dict): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    repository_owner = inputs["repository_owner"]
    repository_name = inputs["repository_name"]
    new_body = inputs["new_body"]
    new_tag_name = inputs["new_tag_name"]
    credential = inputs["credential"]
    
    # Construct the API URL for creating a release
    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/releases"
    
    # Prepare headers with authentication
    headers = {
        "Authorization": f"token {credential.get('token', '')}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Prepare the payload for creating a release
    payload = {
        "tag_name": new_tag_name,
        "body": new_body
    }
    
    # Make the POST request to create the release
    response = requests.post(url, headers=headers, json=payload)
    
    # Check if the response is successful
    if response.status_code == 201:
        # Return None for a successful empty response (though GitHub usually returns a JSON object with the created release)
        return None if response.text.strip() == "" else response.json()
    elif response.status_code in [400, 401, 403, 404, 422]:
        raise Exception(f"Failed to create release. Status code: {response.status_code}, Response: {response.text}")
    else:
        raise Exception(f"Unexpected error occurred while creating release. Status code: {response.status_code}, Response: {response.text}")