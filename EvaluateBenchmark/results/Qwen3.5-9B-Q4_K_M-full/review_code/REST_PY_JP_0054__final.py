import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    try:
        resp = requests.get("https://jsonplaceholder.typicode.com/photos", params={"id": resource_id})
        if resp.status_code != 200:
            raise Exception(f"HTTP {resp.status_code}")
        data = resp.json()
        return data.get("id") if data else None
    except requests.RequestException as e:
        raise Exception(str(e))