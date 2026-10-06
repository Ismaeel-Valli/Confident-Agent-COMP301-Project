import requests
from urllib.parse import quote

def solve(inputs):
    """
    Creates a new label in a GitHub repository using the REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository.
            - new_color (str): Hex color code for the label.
            - new_name (str): Name for the new label.
            - credential (dict): Caller-supplied credentials (token and optional org/user).
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty success.
    
    Raises:
        Exception: If the HTTP request fails.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    color = inputs["new_color"]
    name = inputs["new_name"]
    credentials = inputs["credential"]

    # Construct URL
    url = f"https://api.github.com/repos/{quote(owner)}/{quote(repo)}/labels"

    # Prepare headers with Bearer token authentication
    headers = {
        "Authorization": f"Bearer {credentials['token']}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
        "Content-Type": "application/json"
    }

    # Prepare payload
    payload = {
        "name": name,
        "color": color
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 201:
            # Successful creation; GitHub returns the created label object
            return response.json()
        elif response.status_code == 204:
            # Some endpoints may return 204 No Content on success
            return None
        else:
            raise Exception(f"Failed to create label. Status code: {response.status_code}, Response: {response.text}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error occurred: {str(e)}")