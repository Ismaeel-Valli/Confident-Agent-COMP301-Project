def solve(inputs):
    import requests
    
    base_url = "https://dummyjson.com/users"
    url = f"{base_url}?new_firstName={inputs['new_firstName']}"
    
    response = requests.get(url)
    if response.status_code != 201:
        raise Exception(f"Failed to create user: {response.status_code}")
    
    data = response.json()
    return data.get('id')