import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    try:
        resp = requests.get("https://jsonplaceholder.typicode.com/todos/" + str(resource_id))
        resp.raise_for_status()
        data = resp.json()
        if data is None:
            return None
        title = data.get("title")
        return title
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error: {e}")