import requests
import json

def solve(inputs):
    """
    Update a GitHub organization using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - organization (str): The organization name to update.
            - new_description (str): The new description for the organization.
            - credential (str): Bearer token for authentication.
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
    
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://api.github.com"
    version = "2026-03-10"
    org_name = inputs["organization"]
    new_description = inputs["new_description"]
    credential = inputs["credential"]
    
    # Construct the update URL for organization
    url = f"{base_url}/orgs/{org_name}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": f"application/vnd.github.{version}-preview+json",
        "Content-Type": "application/json"
    }
    
    # Prepare the payload with only the description field to update
    payload = {
        "description": new_description
    }
    
    try:
        response = requests.patch(url, json=payload, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None for successful empty response (204 No Content)
        if response.status_code == 204:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Failed to update organization: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")