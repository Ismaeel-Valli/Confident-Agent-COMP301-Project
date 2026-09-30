import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    url = "https://jsonplaceholder.typicode.com/comments/" + str(resource_id)
    response = requests.delete(url)
    if response.status_code != 200:
        raise Exception(f"Failed to delete comment: {response.status_code}")
    return None