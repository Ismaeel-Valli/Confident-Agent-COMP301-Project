import requests

def solve(inputs):
    base_url = "https://dummyjson.com/users"
    url = f"{base_url}?new_firstName={inputs['new_firstName']}&new_phone={inputs['new_phone']}"
    
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    
    if data.get('status') == 'success':
        return None
    else:
        raise Exception(f"Failed to create user: {data}")