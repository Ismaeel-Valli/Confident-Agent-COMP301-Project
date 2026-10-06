def solve(inputs):
    import requests
    
    resource_id = inputs["resource_id"]
    new_user_identifier = inputs["new_user_identifier"]
    
    url = f"https://jsonplaceholder.typicode.com/albums/{resource_id}"
    payload = {"userId": new_user_identifier}
    
    response = requests.patch(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("id")
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")