import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    url = "https://dummyjson.com/posts/{id}".format(id=resource_id)
    response = requests.delete(url)
    if response.status_code == 204:
        return None
    elif response.status_code >= 400:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    else:
        data = response.json()
        return data.get("id")