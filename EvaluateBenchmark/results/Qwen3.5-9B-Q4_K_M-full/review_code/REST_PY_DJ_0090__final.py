def solve(inputs):
    import requests
    
    resource_id = inputs["resource_id"]
    new_body = inputs["new_body"]
    
    url = "https://dummyjson.com/posts/" + str(resource_id)
    payload = {"body": new_body}
    
    response = requests.put(url, json=payload)
    response.raise_for_status()
    
    data = response.json()
    
    if data.get("statusCode") == 204:
        return None
    
    title = data.get("title")
    return title if title is not None else None