import requests

def solve(inputs):
    base_url = "https://dummyjson.com/users"
    url = f"{base_url}?new_email={inputs['new_email']}&new_firstName={inputs['new_firstName']}"
    
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    
    if 'users' in data and len(data['users']) == 0:
        return None
    
    raise Exception(f"Unexpected response: {data}")