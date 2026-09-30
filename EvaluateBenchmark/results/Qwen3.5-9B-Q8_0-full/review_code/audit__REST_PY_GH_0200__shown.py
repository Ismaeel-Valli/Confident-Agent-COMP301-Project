import requests

def solve(inputs):
    """
    List repository contributors from GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git extension)
            - anon (bool or int): Set to 1 or true to include anonymous contributors
            - page (int): Page number of results to fetch
            - credential (str): Caller-supplied authentication token
    
    Returns:
        list or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    anon = inputs.get("anon", False)
    page = inputs.get("page", 1)
    credential = inputs["credential"]
    
    # Build the base URL for GitHub API v3 (version 2026-03-10)
    base_url = "https://api.github.com"
    
    # Construct the contributors endpoint URL with query parameters
    url = f"{base_url}/repos/{owner}/{repo}/contributors"
    
    # Prepare headers with authentication
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Build query parameters - anon must be a string per contract
    params = {"page": str(page)}
    if anon:
        params["anon"] = "1"
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        # Raise an exception for unsuccessful HTTP responses (4xx, 5xx)
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None for successful empty response
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"GitHub API request failed: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request error: {e}")
    except ValueError as e:
        raise Exception(f"Failed to decode JSON response: {e}")