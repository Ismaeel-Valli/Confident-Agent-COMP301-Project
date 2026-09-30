import requests

def solve(inputs):
    username = inputs["username"]
    page = inputs["page"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/users/{username}/following?page={page}"
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch following list. Status code: {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data