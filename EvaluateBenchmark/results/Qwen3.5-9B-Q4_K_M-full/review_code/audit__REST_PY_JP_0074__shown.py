def solve(inputs):
    import requests
    
    new_title = inputs["new_title"]
    
    url = "https://jsonplaceholder.typicode.com/albums"
    headers = {"Content-Type": "application/json"}
    payload = {"title": new_title}
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create album: {response.status_code}")
    
    data = response.json()
    
    if "title" in data:
        return data["title"]
    elif response.status_code == 201 and len(data) == 0:
        return None
    else:
        return None