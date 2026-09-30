def solve(inputs):
    import requests
    
    resource_id = inputs["resource_id"]
    new_lastName = inputs["new_lastName"]
    
    url = "https://dummyjson.com/users/{id}".format(id=resource_id)
    
    payload = {
        "lastName": new_lastName
    }
    
    response = requests.patch(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update user: {response.status_code} {response.text}")
    
    return response.json()