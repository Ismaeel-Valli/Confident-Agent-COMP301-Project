import requests
from requests.exceptions import RequestException, HTTPError

def solve(inputs):
    """
    Updates an organization's name via the GitHub REST API (version 2026-03-10).
    
    Args:
        inputs (dict): A dictionary containing:
            - 'organization': str, The organization name.
            - 'new_name': str, The new name for the organization.
            - 'credential': dict, Contains authentication details (e.g., token or username/password).
    
    Returns:
        None if the response is empty and successful.
        The decoded JSON response otherwise.
    
    Raises:
        Exception for unsuccessful HTTP responses.
    """
    org_name = inputs['organization']
    new_name = inputs['new_name']
    credential = inputs['credential']
    
    # Construct the API URL for updating an organization
    url = f"https://api.github.com/orgs/{org_name}"
    
    # Prepare headers with authentication
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'X-GitHub-Api-Version': '2026-03-10'
    }
    
    # Determine authentication method based on credential structure
    if 'token' in credential:
        headers['Authorization'] = f'token {credential["token"]}'
    elif 'username' in credential and 'password' in credential:
        auth = (credential['username'], credential['password'])
    else:
        raise ValueError("Credential must contain either a 'token' or both 'username' and 'password'.")
    
    # Prepare the payload for updating the organization name
    payload = {
        "name": new_name
    }
    
    try:
        response = requests.put(url, headers=headers, json=payload)
        
        # Raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()
        
        # Return None if the response is empty (successful update with no content)
        if not response.text:
            return None
        
        # Decode and return the JSON response
        return response.json()
    
    except HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except RequestException as req_err:
        raise Exception(f"Request error occurred: {req_err}")