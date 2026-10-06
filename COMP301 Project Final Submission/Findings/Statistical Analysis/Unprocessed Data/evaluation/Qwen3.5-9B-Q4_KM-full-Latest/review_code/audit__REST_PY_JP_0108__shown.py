import requests

def solve(inputs):
    new_title = inputs["new_title"]
    new_url = inputs["new_url"]
    
    url = "https://jsonplaceholder.typicode.com/photos"
    payload = {"title": new_title, "url": new_url}
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to submit photo: {response.status_code}")
    
    data = response.json()
    
    if "id" in data:
        return data["id"]
    else:
        return None