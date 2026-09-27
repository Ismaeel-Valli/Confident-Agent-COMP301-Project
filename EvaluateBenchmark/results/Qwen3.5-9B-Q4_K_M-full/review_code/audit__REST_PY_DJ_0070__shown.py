def solve(inputs):
    import requests
    resource_id = inputs["resource_id"]
    url = "https://dummyjson.com/posts/" + str(resource_id)
    response = requests.delete(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("isDeleted")
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")