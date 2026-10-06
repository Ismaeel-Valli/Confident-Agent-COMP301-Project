import requests

def solve(inputs):
    resource_id = inputs.get("resource_id")
    
    url = f"https://dummyjson.com/products/{resource_id}"
    response = requests.delete(url)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    if "isDeleted" in data and data["isDeleted"]:
        return data["isDeleted"]
    
    if not data:
        return None
    
    return None