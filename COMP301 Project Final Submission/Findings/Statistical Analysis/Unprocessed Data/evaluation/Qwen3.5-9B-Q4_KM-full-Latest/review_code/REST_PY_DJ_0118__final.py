import requests

def solve(inputs):
    base_url = "https://dummyjson.com/users"
    url = f"{base_url}?new_firstName={inputs['new_firstName']}&new_phone={inputs['new_phone']}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data.get('users'):
        return None
    
    return data['users'][0]