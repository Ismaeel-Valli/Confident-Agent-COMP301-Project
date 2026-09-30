def solve(inputs):
    import requests
    
    resource_id = inputs["resource_id"]
    new_email = inputs["new_email"]
    
    url = "https://dummyjson.com/users/{0}".format(resource_id)
    response = requests.put(url, json={"email": new_email})
    
    if response.status_code == 200:
        return None
    elif response.status_code == 404:
        return None
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")