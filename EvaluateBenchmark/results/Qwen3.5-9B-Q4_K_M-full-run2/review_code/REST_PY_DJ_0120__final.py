import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    new_user_identifier = inputs["new_user_identifier"]
    
    url = "https://dummyjson.com/posts/{id}".format(id=resource_id)
    headers = {"Content-Type": "application/json"}
    payload = {"user_id": new_user_identifier}
    
    response = requests.put(url, json=payload, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    if data.get("statusCode") == 204:
        return None
    
    title = data.get("title")
    return title