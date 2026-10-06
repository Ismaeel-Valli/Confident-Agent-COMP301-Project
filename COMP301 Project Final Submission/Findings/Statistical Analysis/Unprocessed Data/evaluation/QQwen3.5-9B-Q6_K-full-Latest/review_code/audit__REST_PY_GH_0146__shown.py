def solve(inputs):
    """
    List repository issues from GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Must contain:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Repository name without .git extension
            - type (str, optional): Issue type to filter by
            - credential (str): Bearer token for authentication
    
    Returns:
        list or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Build the API URL
    base_url = "https://api.github.com"
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    issue_type = inputs.get("type")
    
    # Construct the endpoint for listing issues
    url = f"{base_url}/repos/{owner}/{repo}/issues"
    
    # Prepare headers with authentication
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Add issue type filter if provided
    params = {}
    if issue_type:
        params["state"] = "all"  # Default to all states when filtering by type
        params["labels"] = issue_type
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        # Raise exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode JSON response
        data = response.json()
        
        # Return None for empty successful response
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"GitHub API request failed: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request error: {e}")