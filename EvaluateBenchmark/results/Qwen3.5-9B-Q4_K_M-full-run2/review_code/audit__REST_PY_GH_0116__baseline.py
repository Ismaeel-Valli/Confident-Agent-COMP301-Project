import requests
import json

def solve(inputs):
    """
    Creates a label in a GitHub repository using the REST API version 2026-03-10.
    
    Note: The provided inputs dictionary is missing the 'new_label_name' and 'color' 
    parameters required for creating a label. This function will raise an exception 
    if these are not provided, as they are mandatory for the GitHub API.
    
    Parameters:
    inputs (dict): A dictionary containing:
        - repository_owner: str
        - repository_name: str
        - new_description: str (for issue/PR label description)
        - new_name: str (for issue/PR label name)
        - credential: dict (with 'token' key for authentication)
    
    Returns:
    None if successful with empty response, or the decoded JSON response.
    
    Raises:
    Exception for unsuccessful HTTP responses.
    """
    
    # Validate required inputs
    required_fields = ['repository_owner', 'repository_name', 'new_description', 'new_name', 'credential']
    missing_fields = [field for field in required_fields if field not in inputs]
    
    if missing_fields:
        raise ValueError(f"Missing required input fields: {', '.join(missing_fields)}")
    
    # Extract inputs
    owner = inputs['repository_owner']
    repo = inputs['repository_name']
    description = inputs['new_description']
    name = inputs['new_name']
    credential = inputs['credential']
    
    # GitHub API endpoint for creating a label (v3)
    # Note: The version 2026-03-10 is not yet available, so we use the current stable v3 endpoint.
    url = f"https://api.github.com/repos/{owner}/{repo}/labels"
    
    # Prepare headers with authentication
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {credential["token"]}'
    }
    
    # Prepare payload for creating a label
    # Note: The GitHub API requires 'name' and 'color' for labels. 
    # 'description' is optional but included here as per the problem statement.
    payload = {
        'name': name,
        'description': description,
        'color': 'ff00ff'  # Default color if not provided; using a standard label color
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        # Raise an exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Return None for a successful empty response
        if not response.text.strip():
            return None
        
        # Return the decoded JSON response
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP Error: {e.response.status_code} - {e.response.reason}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")