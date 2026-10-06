import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    url = f"https://dummyjson.com/posts/{resource_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("post")
    else:
        raise Exception(f"Failed to retrieve post. Status code: {response.status_code}")