def solve(inputs):
    import requests
    
    resource_id = inputs["resource_id"]
    new_title = inputs["new_title"]
    
    url = f"https://jsonplaceholder.typicode.com/photos/{resource_id}"
    payload = {"title": new_title}
    
    response = requests.put(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    data = response.json()
    return data.get("title")