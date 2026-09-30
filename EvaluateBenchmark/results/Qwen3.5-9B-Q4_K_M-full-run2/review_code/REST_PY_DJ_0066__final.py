import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    new_lastName = inputs["new_lastName"]
    
    url = "https://dummyjson.com/users/{0}/update".format(resource_id)
    payload = {"lastName": new_lastName}
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return data.get("id")
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"Failed to update user: {response.status_code}")