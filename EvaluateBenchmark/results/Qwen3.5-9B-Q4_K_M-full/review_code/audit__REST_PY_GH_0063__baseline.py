import requests

def solve(inputs):
    """
    Lists the people a GitHub user follows using the GitHub REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'username' (str): The handle for the GitHub user account.
            - 'credential' (dict): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response if successful, or None for an empty list of follows.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    username = inputs['username']
    credential = inputs['credential']
    
    # Construct the API URL for following users (v3 endpoint)
    url = f"https://api.github.com/users/{username}/following"
    
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Prepare authentication using the provided credential
    # Assuming 'credential' contains a token or auth method compatible with requests
    if isinstance(credential, dict):
        if 'token' in credential:
            headers['Authorization'] = f'token {credential["token"]}'
        elif 'username' in credential and 'password' in credential:
            # Basic Auth fallback if token is not present
            auth = (credential['username'], credential['password'])
    else:
        raise ValueError("Credential must be a dictionary containing either 'token' or 'username'/'password'.")

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for an empty list of follows
    if not data:
        return None
    
    return data