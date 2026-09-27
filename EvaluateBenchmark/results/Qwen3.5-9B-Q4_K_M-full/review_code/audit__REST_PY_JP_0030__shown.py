import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    url = "https://jsonplaceholder.typicode.com/todos/" + str(resource_id)
    response = requests.delete(url)
    if response.status_code != 204:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} {response.text}")
    return None