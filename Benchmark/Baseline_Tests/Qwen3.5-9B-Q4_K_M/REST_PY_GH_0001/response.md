```python
import requests
import json

def solve(inputs):
    """
    Fetches an organization from the GitHub REST API (version 2026-03-10).
    
    Args:
        inputs (dict): A dictionary containing:
            - 'organization' (str): The name of the organization.
            - 'credential' (str): The caller-supplied credential (e.g., token or Bearer string).
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, 
                      or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful status code.
    """
    org_name = inputs["organization"]
    credential = inputs["credential"]
    
    # GitHub API endpoint for getting an organization
    url = f"https://api.github.com/orgs/{org_name}"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # Return None for a successful empty response (though GitHub orgs are rarely empty JSON objects)
        return data if data else None
    elif response.status_code in [401, 403]:
        raise Exception(f"Authentication or permission error: {response.status_code}")
    elif response.status_code == 404:
        raise Exception(f"Organization not found: {org_name}")
    else:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
```