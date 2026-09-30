import requests

def solve(inputs):
    username = inputs["username"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/user/{username}/following"
    headers = {
        "Authorization": f"token {credential}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch following users for {username}: HTTP {response.status_code}, {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data