def solve(inputs):
    import requests
    
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    base = inputs["new_base"]
    body = inputs["new_body"]
    head = inputs["new_head"]
    title = inputs["new_title"]
    cred = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    
    headers = {
        "Authorization": f"token {cred}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {
        "base": base,
        "body": body,
        "head": head,
        "title": title
    }
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 201:
        return None
    
    return response.json()