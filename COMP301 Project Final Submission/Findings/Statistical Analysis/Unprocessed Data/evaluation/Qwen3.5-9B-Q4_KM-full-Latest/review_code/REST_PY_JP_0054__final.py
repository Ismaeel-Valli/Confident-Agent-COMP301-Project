import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    try:
        resp = requests.get("https://jsonplaceholder.typicode.com/photos", params={"id": resource_id})
        resp.raise_for_status()
        data = resp.json()
        if "id" in data:
            return data["id"]
        else:
            return None
    except requests.HTTPError as e:
        raise e