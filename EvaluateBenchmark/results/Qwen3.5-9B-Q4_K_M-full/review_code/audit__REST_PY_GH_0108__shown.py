def solve(inputs):
    """
    Get a commit from GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - page_size (int): Number of results per page (max 100)
            - ref (str): Commit reference
            - credential (str): Caller-supplied credential (assumed to have necessary permissions)
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Build the API URL
    base_url = "https://api.github.com"
    endpoint = f"/repos/{inputs['repository_owner']}/{inputs['repository_name']}/commits"
    
    # Prepare headers with authentication
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    # Build query parameters
    params = {
        "per_page": inputs["page_size"]
    }
    
    # Make the request
    response = requests.get(
        base_url + endpoint,
        headers=headers,
        params=params
    )
    
    # Raise exception for unsuccessful HTTP responses
    if not response.ok:
        raise Exception(f"GitHub API returned status {response.status_code}: {response.text}")
    
    # Decode and return the JSON response
    json_response = response.json()
    
    # Return None for successful empty response
    if len(json_response) == 0:
        return None
    
    return json_response