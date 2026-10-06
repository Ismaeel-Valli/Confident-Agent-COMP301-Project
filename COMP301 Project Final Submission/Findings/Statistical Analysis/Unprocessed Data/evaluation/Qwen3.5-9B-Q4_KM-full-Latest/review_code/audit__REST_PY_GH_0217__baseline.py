import requests

def solve(inputs):
    """
    Lists repositories for a GitHub user based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'username' (str): The GitHub username.
            - 'type' (str, optional): Type of repository ('all', 'owner', or 'public').
            - 'sort' (str, optional): Property to sort by ('created', 'updated', etc.).
            - 'credential' (dict): Contains authentication details (e.g., token).
    
    Returns:
        dict or None: Decoded JSON response if successful. Returns None for an empty list.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    username = inputs['username']
    repo_type = inputs.get('type', 'all')
    sort_by = inputs.get('sort', 'updated')
    credential = inputs['credential']

    # Construct the API URL for GitHub REST API version 2026-03-10
    base_url = "https://api.github.com"
    url = f"{base_url}/users/{username}/repos"

    # Build query parameters
    params = {
        'type': repo_type,
        'sort': sort_by
    }

    # Prepare headers with authentication
    headers = {
        'Accept': 'application/vnd.github+json'
    }

    # Add authorization header if a token is provided in the credential
    if 'token' in credential:
        headers['Authorization'] = f"Bearer {credential['token']}"

    try:
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve repositories. Status code: {response.status_code}, Response: {response.text}")
        
        data = response.json()
        
        # Return None for an empty list
        if not data:
            return None
        
        return data

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")