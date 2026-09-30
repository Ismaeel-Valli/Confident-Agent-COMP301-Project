import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    new_title = inputs["new_title"]
    
    url = "https://jsonplaceholder.typicode.com/albums/" + str(resource_id)
    response = requests.put(url, json={"title": new_title})
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    return data.get("title")