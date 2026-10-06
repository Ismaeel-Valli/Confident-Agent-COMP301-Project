import requests

def solve(inputs):
    base_url = "https://dummyjson.com/posts/add"
    url = f"{base_url}"
    
    payload = {
        "body": inputs["new_body"],
        "title": inputs["new_title"],
        "userId": inputs["new_user_identifier"]
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    data = response.json()
    
    if data.get("success") is True:
        return None
    
    raise Exception(f"Unexpected response: {data}")