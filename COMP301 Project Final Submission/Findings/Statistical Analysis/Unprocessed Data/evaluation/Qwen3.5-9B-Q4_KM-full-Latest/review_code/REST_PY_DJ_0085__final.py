import requests

def solve(inputs):
    base_url = "https://dummyjson.com/products/add"
    new_description = inputs["new_description"]
    new_title = inputs["new_title"]
    
    payload = {
        "description": new_description,
        "title": new_title
    }
    
    response = requests.post(base_url, json=payload)
    response.raise_for_status()
    
    data = response.json()
    if data.get("statusCode") == 201 and data.get("products") is None:
        return None
    
    return data.get("title")