import requests

def solve(inputs):
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/posts"
    
    payload = {"title": inputs["new_title"]}
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 201:
        return None
    else:
        raise Exception(f"Failed to create post. Status code: {response.status_code}")