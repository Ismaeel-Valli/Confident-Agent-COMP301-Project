def solve(inputs):
    import requests
    
    resource_id = inputs["resource_id"]
    new_firstName = inputs["new_firstName"]
    
    url = f"https://dummyjson.com/users/{resource_id}"
    payload = {"firstName": new_firstName}
    
    response = requests.put(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("id")
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"Failed to update user: {response.status_code} - {response.text}")