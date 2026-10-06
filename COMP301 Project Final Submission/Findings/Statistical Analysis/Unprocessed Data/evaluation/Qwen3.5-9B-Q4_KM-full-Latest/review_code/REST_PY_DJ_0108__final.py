def solve(inputs):
    import requests
    
    base_url = "https://dummyjson.com/users/add"
    url = f"{base_url}?new_email={inputs['new_email']}&new_firstName={inputs['new_firstName']}"
    
    response = requests.post(url)
    
    if response.status_code == 201:
        data = response.json()
        return data.get('id')
    elif response.status_code == 200:
        return None
    else:
        raise Exception(f"Failed to create user: {response.status_code} - {response.text}")