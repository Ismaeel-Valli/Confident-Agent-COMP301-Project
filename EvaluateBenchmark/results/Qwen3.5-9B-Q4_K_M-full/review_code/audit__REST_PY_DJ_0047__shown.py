import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    url = "https://dummyjson.com/products/{id}".format(id=resource_id)
    response = requests.delete(url)
    if response.status_code == 200:
        data = response.json()
        return None
    elif response.status_code == 404:
        data = response.json()
        return data.get("title")
    else:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")