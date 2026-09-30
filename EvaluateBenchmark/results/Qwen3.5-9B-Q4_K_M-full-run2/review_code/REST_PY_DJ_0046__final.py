import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    new_title = inputs["new_title"]
    
    url = "https://dummyjson.com/products/{id}".format(id=resource_id)
    response = requests.put(url, json={"title": new_title})
    
    if response.status_code == 200:
        data = response.json()
        if data.get("isSuccessful"):
            return data.get("product", {}).get("title")
        else:
            raise Exception("Failed to update product")
    elif response.status_code == 404:
        return None
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")