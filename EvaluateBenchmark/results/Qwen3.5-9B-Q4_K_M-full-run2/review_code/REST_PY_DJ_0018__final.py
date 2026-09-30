import requests

def solve(inputs):
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
    if not data.get("posts"):
        return None
    return data