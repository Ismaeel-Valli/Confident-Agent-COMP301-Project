import requests
import base64

def solve(inputs):
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    assignee = inputs.get("assignee")
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    params = {}
    if assignee:
        params["assignee"] = assignee
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
    
    return data