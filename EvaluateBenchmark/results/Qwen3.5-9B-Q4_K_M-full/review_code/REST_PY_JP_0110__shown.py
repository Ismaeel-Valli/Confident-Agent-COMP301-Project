def solve(inputs):
    import requests
    
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/todos"
    
    payload = {
        "title": inputs["new_title"],
        "body": "",
        "userId": 1
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create todo: HTTP {response.status_code}")
    
    data = response.json()
    
    if "id" in data:
        return data["id"]
    else:
        return None