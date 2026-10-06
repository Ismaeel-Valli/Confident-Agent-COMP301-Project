def solve(inputs):
    import requests
    
    resource_id = inputs["resource_id"]
    new_title = inputs["new_title"]
    
    url = "https://dummyjson.com/products/{0}".format(resource_id)
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": new_title
    }
    
    response = requests.put(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception("Unsuccessful HTTP response")
    
    data = response.json()
    
    if "product" in data and "title" in data["product"]:
        return data["product"]["title"]
    elif data.get("statusCode") == 204:
        return None
    else:
        return None