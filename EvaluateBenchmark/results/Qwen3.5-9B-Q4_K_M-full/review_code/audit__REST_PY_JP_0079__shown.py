def solve(inputs):
    import requests
    
    resource_id = inputs.get("resource_id")
    if resource_id is None:
        raise ValueError("Missing required key 'resource_id' in inputs")
    
    url = f"https://jsonplaceholder.typicode.com/photos/{resource_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    title = data.get("title")
    return title if title is not None else None