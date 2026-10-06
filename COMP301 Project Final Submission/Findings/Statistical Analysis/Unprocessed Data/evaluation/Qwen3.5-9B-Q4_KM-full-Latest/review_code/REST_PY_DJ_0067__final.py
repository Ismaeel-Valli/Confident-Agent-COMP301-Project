def solve(inputs):
    import requests
    
    base_url = "https://dummyjson.com/users/add"
    url = f"{base_url}?new_firstName={inputs['new_firstName']}&new_lastName={inputs['new_lastName']}"
    
    response = requests.post(url)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create user. Status code: {response.status_code}")
    
    data = response.json()
    
    if 'id' in data and data['id'] is not None:
        return data['id']
    elif data.get('status') == 'success':
        return None
    else:
        raise Exception("Unexpected response structure")