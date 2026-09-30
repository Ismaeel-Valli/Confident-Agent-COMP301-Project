import requests

def solve(inputs):
    base_url = "https://dummyjson.com/users/add"
    url = f"{base_url}?new_firstName={inputs['new_firstName']}&new_lastName={inputs['new_lastName']}"
    
    response = requests.post(url)
    response.raise_for_status()
    
    data = response.json()
    
    if 'id' in data:
        return data['id']
    elif response.status_code == 201:
        return None
    else:
        raise Exception(f"Failed to create user: {response.text}")