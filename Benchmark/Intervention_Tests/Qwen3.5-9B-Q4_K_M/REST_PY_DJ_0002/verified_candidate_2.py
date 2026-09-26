import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    url = f"https://dummyjson.com/products/{resource_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("title") if data else None
    elif response.status_code in (404,):
        return None
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")