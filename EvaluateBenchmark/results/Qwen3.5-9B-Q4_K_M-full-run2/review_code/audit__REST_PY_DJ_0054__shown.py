def solve(inputs):
    import requests
    
    resource_id = inputs["resource_id"]
    url = f"https://dummyjson.com/posts/{resource_id}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    title = data.get("title")
    return title