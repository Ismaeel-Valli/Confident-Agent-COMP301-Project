import requests

def solve(inputs):
    resource_id = inputs.get("resource_id")
    url = f"https://dummyjson.com/todos/{resource_id}"
    response = requests.delete(url)
    if response.status_code == 204:
        return None
    elif response.status_code == 404:
        return None
    else:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")