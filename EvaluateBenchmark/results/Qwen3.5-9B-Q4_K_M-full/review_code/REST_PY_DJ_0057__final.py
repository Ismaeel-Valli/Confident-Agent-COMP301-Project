def solve(inputs):
    import requests
    
    base_url = "https://dummyjson.com/posts/add"
    new_body = inputs["new_body"]
    new_title = inputs["new_title"]
    new_user_identifier = inputs["new_user_identifier"]
    
    payload = {
        "body": new_body,
        "title": new_title,
        "userId": new_user_identifier
    }
    
    response = requests.post(base_url, json=payload)
    response.raise_for_status()
    
    data = response.json()
    
    if data.get("statusCode") == 201:
        title = data.get("title")
        return title if title is not None else None
    elif data.get("statusCode") == 400:
        return None
    else:
        raise Exception(f"Failed to create post. Status code: {data.get('statusCode')}")