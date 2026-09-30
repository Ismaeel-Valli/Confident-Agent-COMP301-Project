import requests

def solve(inputs):
    username = inputs["username"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/users/{username}/following"
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch following list for user '{username}': HTTP {response.status_code}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data