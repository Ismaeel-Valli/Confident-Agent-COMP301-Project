import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    url = f"https://dummyjson.com/posts/{resource_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("posts", [])
    else:
        raise Exception(f"HTTP {response.status_code}")