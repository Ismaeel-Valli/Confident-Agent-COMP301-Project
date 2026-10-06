import requests

def solve(inputs):
    """
    Get an organization from GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - "organization": The organization name (str)
            - "credential": Caller-supplied credential (str, assumed to have necessary permissions)
    
    Returns:
        dict or None: Decoded JSON response for successful request. Returns None for empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.github.com"
    organization = inputs["organization"]
    credential = inputs["credential"]
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {credential}"
    }
    
    url = f"{base_url}/orgs/{organization}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"Failed to get organization {organization}: HTTP {response.status_code}")