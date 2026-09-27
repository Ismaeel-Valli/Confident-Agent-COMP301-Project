import requests
import json

def solve(inputs):
    """
    Create an organization repository on GitHub using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - organization (str): The organization name.
            - new_homepage (str): Value for the homepage attribute.
            - new_name (str): Value for the name attribute.
            - credential (str): Caller-supplied authentication token.
    
    Returns:
        None if successful (empty response), otherwise decoded JSON response.
    
    Raises:
        Exception on unsuccessful HTTP response.
    """
    base_url = "https://api.github.com"
    url = f"{base_url}/orgs/{inputs['organization']}/repos"
    
    headers = {
        "Authorization": f"token {inputs['credential']}",
        "Accept": "application/vnd.github+json"
    }
    
    data = {
        "name": inputs["new_name"],
        "homepage": inputs["new_homepage"]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return None
    elif response.status_code == 422:
        return response.json()
    else:
        raise Exception(f"Failed to create repository. Status code: {response.status_code}, Response: {response.text}")