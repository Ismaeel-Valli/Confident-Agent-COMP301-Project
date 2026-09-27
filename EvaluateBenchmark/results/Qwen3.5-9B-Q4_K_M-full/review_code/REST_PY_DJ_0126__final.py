def solve(inputs):
    import requests
    
    resource_id = inputs['resource_id']
    new_phone = inputs['new_phone']
    
    url = "https://dummyjson.com/users/{0}/contact".format(resource_id)
    payload = {"phone": new_phone}
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    if 'id' in data:
        return data['id']
    else:
        return None