import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    url = "https://jsonplaceholder.typicode.com/photos/" + str(resource_id)
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"HTTP error {response.status_code} for photo {resource_id}")
    data = response.json()
    if not data:
        return None
    return data.get("title")