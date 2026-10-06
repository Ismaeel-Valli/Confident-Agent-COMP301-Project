import requests

def solve(inputs):
    """
    Lists the people a GitHub user follows using the GitHub REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'username' (str): The handle for the GitHub user account.
            - 'credential' (dict): Caller-supplied credential with necessary permissions 
                                  (assumed to contain 'token' key for Authorization).
    
    Returns:
        dict or None: Decoded JSON response if data exists, None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses (non-2xx status codes).
    """
    username = inputs['username']
    credential = inputs['credential']
    
    # Construct the API URL for following users
    url = f"https://api.github.com/users/{username}/following"
    
    headers = {
        'Accept': 'application/vnd.github+json'
    }
    
    # Add authorization header if token is present in credential
    if 'token' in credential:
        headers['Authorization'] = f'Bearer {credential["token"]}'
    
    response = requests.get(url, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    data = response.json()
    
    # Return None for successful empty response (empty list)
    if not data:
        return None
    
    return data