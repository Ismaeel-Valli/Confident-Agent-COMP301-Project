import requests


def solve(inputs):
    """Submit a new post to JSONPlaceholder using provided title and body."""
    url = "https://jsonplaceholder.typicode.com/posts"
    
    response = requests.post(url, json={
        "title": inputs["new_title"],
        "body": inputs["new_body"]
    })
    
    if response.status_code != 201:
        raise Exception(f"Failed to create post. Status code: {response.status_code}")
    
    return None