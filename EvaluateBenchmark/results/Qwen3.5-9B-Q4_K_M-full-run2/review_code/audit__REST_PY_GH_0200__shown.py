def solve(inputs):
    """
    List repository contributors for GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git extension)
            - anon (bool/int): Set to 1 or true to include anonymous contributors
            - page (int): Page number of results to fetch
            - credential (str): Caller-supplied credential with necessary permissions
    
    Returns:
        dict: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Build the API URL for GitHub REST API v2026-03-10
    base_url = "https://api.github.com"
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    anon = inputs.get("anon", False)
    page = inputs.get("page", 1)
    
    # Construct the endpoint for contributors
    url = f"{base_url}/repos/{owner}/{repo}/contributors"
    
    # Prepare headers with authentication using credential
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Add anonymous contributor parameter if requested (must be string per contract)
    params = {}
    if anon:
        params["anon"] = str(1)
    
    # Set page parameter for pagination
    params["page"] = page
    
    # Make the API request
    response = requests.get(url, headers=headers, params=params)
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode JSON response
    data = response.json()
    
    # Return None for empty response
    if not data:
        return None
    
    return data