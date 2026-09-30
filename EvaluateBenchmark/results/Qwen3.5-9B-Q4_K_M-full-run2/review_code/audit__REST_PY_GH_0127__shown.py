def solve(inputs):
    """
    Create a release on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - new_name (str): New name for the release
            - new_tag_name (str): Tag name for the release
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Build the API URL for creating a release
    base_url = "https://api.github.com"
    url = f"{base_url}/repos/{inputs['repository_owner']}/{inputs['repository_name']}/releases"
    
    # Prepare headers with authentication
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Prepare the payload for creating a release
    payload = {
        "tag_name": inputs['new_tag_name'],
        "name": inputs['new_name']
    }
    
    # Make the POST request to create the release
    response = requests.post(url, headers=headers, json=payload)
    
    # Check if the request was successful
    if response.status_code not in [201, 202]:  # 201 Created or 202 Accepted
        response.raise_for_status()
    
    # Return the decoded JSON response
    return response.json()