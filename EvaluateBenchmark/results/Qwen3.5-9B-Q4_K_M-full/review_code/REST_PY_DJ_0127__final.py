def solve(inputs):
    import requests
    
    base_url = "https://dummyjson.com/users"
    url = f"{base_url}?new_firstName={inputs['new_firstName']}&new_phone={inputs['new_phone']}"
    
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    
    if 'id' in data:
        return data['id']
    elif response.status_code == 200:
        return None
    
    raise Exception(f"Failed to create user: {response.status_code} - {data}")