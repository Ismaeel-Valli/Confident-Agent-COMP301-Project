def solve(inputs):
    import requests
    
    resource_id = inputs["resource_id"]
    new_price = inputs["new_price"]
    
    url = "https://dummyjson.com/products/{0}".format(resource_id)
    payload = {"price": new_price}
    
    response = requests.put(url, json=payload)
    
    if response.status_code == 200:
        return None
    else:
        raise Exception("Unsuccessful HTTP response")