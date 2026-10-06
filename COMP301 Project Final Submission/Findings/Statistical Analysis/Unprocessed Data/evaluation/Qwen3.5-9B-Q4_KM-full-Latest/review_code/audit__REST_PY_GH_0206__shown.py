import requests

def solve(inputs):
    """
    Update a label on a GitHub repository using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - name (str): Label name to update
            - new_color (str): New color value for the label
            - new_description (str): New description value for the label
            - credential (str): Bearer token for authentication
    
    Returns:
        None if successful with empty response, otherwise decoded JSON response.
    
    Raises:
        Exception for unsuccessful HTTP responses.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    label_name = inputs["name"]
    new_color = inputs["new_color"]
    new_description = inputs["new_description"]
    credential = inputs["credential"]
    
    url = "https://api.github.com/repos/{owner}/{repo}/labels/{name}".format(
        owner=owner,
        repo=repo,
        name=label_name
    )
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {
        "color": new_color,
        "description": new_description
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to update label: {response.status_code} - {response.text}")
    
    return response.json() if response.status_code != 204 else None