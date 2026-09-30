import requests

def solve(inputs):
    """Retrieve a post by identifier from DummyJSON."""
    resource_id = inputs["resource_id"]
    url = f"https://dummyjson.com/posts/{resource_id}"
    
    response = requests.get(url)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return data.get("post")
    else:
        raise Exception(f"Failed to retrieve post: {response.status_code}")