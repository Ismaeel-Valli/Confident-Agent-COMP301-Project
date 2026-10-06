def solve(inputs):
    import requests
    
    resource_id = inputs["resource_id"]
    url = "https://jsonplaceholder.typicode.com/comments/" + str(resource_id)
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    if data is None:
        return None
    
    name = data.get("name")
    return name