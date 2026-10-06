import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    new_body = inputs["new_body"]
    
    url = "https://dummyjson.com/posts/{id}".format(id=resource_id)
    payload = {"body": new_body}
    
    response = requests.patch(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    return response.json()