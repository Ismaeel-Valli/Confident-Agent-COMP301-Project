import requests

def solve(inputs):
    base_url = "https://dummyjson.com/products/add"
    
    payload = {
        "title": inputs["new_title"],
        "price": inputs["new_price"]
    }
    
    response = requests.post(base_url, json=payload)
    
    if response.status_code == 201:
        return response.json().get("id")
    elif response.status_code == 200:
        return None
    else:
        raise Exception(f"Failed to create product. Status code: {response.status_code}")