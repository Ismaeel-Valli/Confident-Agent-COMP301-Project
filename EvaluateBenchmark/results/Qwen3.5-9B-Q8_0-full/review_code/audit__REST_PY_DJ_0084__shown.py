import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    new_description = inputs["new_description"]
    
    base_url = "https://dummyjson.com/products"
    url = f"{base_url}/{resource_id}"
    
    payload = {
        "description": new_description
    }
    
    try:
        response = requests.put(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        
        if "title" in data and data["title"] is not None:
            return data["title"]
        else:
            return None
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")