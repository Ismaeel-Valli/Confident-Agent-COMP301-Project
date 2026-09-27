import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    url = "https://jsonplaceholder.typicode.com/comments/" + str(resource_id)
    response = requests.delete(url)
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    data = response.json()
    if not data:
        return None
    return data