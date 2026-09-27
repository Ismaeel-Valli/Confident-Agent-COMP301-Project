import requests

def solve(inputs):
    resource_id = inputs.get("resource_id")
    
    url = f"https://dummyjson.com/posts/{resource_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    # Check for successful empty response (e.g., {"posts": []})
    if not data.get("posts"):
        return None
    
    post = data["posts"][0]
    
    # Return the id value, or None if absent
    return post.get("id")