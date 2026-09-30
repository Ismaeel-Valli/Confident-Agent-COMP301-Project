import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    url = "https://dummyjson.com/posts/{id}".format(id=resource_id)
    response = requests.delete(url)
    if response.status_code != 200:
        raise Exception(f"Failed to delete post: {response.status_code}")
    return None