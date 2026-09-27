import requests

def solve(inputs):
    """
    Creates an issue in a GitHub repository using the REST API.
    
    Parameters:
    inputs (dict): A dictionary containing the following keys:
        - repository_owner (str): The account owner of the repository.
        - repository_name (str): The name of the repository without the .git extension.
        - new_assignees (list): Value for the assignees attribute.
        - new_body (str): Value for the body attribute.
        - new_labels (list): Value for the labels attribute.
        - new_title (str): Value for the title attribute.
        - credential (dict): Caller-supplied credential with necessary permissions.
    
    Returns:
    dict or None: The decoded JSON response if successful, or None for a successful empty response.
    
    Raises:
    Exception: If the HTTP response is unsuccessful.
    """
    
    # Construct the URL for creating an issue
    url = f"https://api.github.com/repos/{inputs['repository_owner']}/{inputs['repository_name']}/issues"
    
    # Prepare the headers with authentication
    headers = {
        'Authorization': f'Bearer {inputs["credential"]["token"]}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2026-03-10'
    }
    
    # Prepare the payload for creating an issue
    payload = {
        "title": inputs['new_title'],
        "body": inputs['new_body'],
        "assignees": inputs['new_assignees'] if inputs['new_assignees'] else None,
        "labels": inputs['new_labels'] if inputs['new_labels'] else None
    }
    
    # Send the POST request to create the issue
    response = requests.post(url, headers=headers, json=payload)
    
    # Check if the request was successful
    if response.status_code == 201:
        return None  # Return None for a successful empty response
    elif response.status_code == 422:
        # Handle validation errors (e.g., invalid labels or assignees)
        raise Exception(f"Validation error: {response.json()}")
    else:
        # Raise an exception for any other unsuccessful HTTP response
        raise Exception(f"Failed to create issue. Status code: {response.status_code}, Response: {response.text}")

# Example usage (not executed):
# inputs = {
#     "repository_owner": "octocat",
#     "repository_name": "Hello-World",
#     "new_assignees": ["octocat"],
#     "new_body": "This is a new issue.",
#     "new_labels": ["bug", "help wanted"],
#     "new_title": "Fix the bug",
#     "credential": {
#         "token": "YOUR_GITHUB_TOKEN"
#     }
# }
# result = solve(inputs)