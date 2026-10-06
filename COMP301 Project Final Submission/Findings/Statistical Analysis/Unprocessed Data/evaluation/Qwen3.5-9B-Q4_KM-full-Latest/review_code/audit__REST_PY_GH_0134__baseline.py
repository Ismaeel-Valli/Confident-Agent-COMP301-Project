import requests

def solve(inputs):
    """
    Lists followers of a GitHub user using the GitHub REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'username' (str): The GitHub username.
            - 'page' (int): The page number of results to fetch.
            - 'credential' (dict): Contains authentication details (e.g., token).
    
    Returns:
        dict or None: Decoded JSON response if successful, or None for an empty list.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    username = inputs['username']
    page = inputs['page']
    credential = inputs['credential']
    
    # Construct the API URL for listing followers
    url = f"https://api.github.com/users/{username}/followers"
    
    # Prepare headers with authentication
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Add authorization header based on credential type (assuming token for now)
    if 'token' in credential:
        headers["Authorization"] = f"Bearer {credential['token']}"
    elif 'username' in credential and 'password' in credential:
        # Basic auth fallback if token is not provided
        import base64
        auth_string = f"{credential['username']}:{credential['password']}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        headers["Authorization"] = f"Basic {encoded_auth}"
    else:
        raise ValueError("Credential must contain either 'token' or ('username' and 'password').")
    
    # Add pagination parameter
    params = {"page": page}
    
    # Make the request
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch followers: HTTP {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    # Return None for an empty list
    if not data:
        return None
    
    return data