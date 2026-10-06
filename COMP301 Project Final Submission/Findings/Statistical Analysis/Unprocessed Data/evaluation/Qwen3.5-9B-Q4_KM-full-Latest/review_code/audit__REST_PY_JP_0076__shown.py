def solve(inputs):
    import requests
    
    resource_id = inputs["resource_id"]
    new_title = inputs["new_title"]
    new_user_identifier = inputs["new_user_identifier"]
    
    url = f"https://jsonplaceholder.typicode.com/albums/{resource_id}"
    payload = {
        "title": new_title,
        "userId": new_user_identifier
    }
    
    response = requests.put(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    title = data.get("title")
    return title if title is not None else None