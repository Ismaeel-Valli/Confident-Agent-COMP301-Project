import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    new_email = inputs["new_email"]
    
    url = "https://jsonplaceholder.typicode.com/comments/" + str(resource_id)
    
    response = requests.patch(url, json={"email": new_email})
    
    if response.status_code != 200:
        raise Exception(f"Failed to update comment: {response.status_code}")
    
    data = response.json()
    
    if "name" in data and data["name"] is not None:
        return data["name"]
    elif response.status_code == 204 or (isinstance(data, dict) and len(data) == 0):
        return None
    else:
        return None