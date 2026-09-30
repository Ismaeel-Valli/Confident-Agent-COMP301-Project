def solve(inputs):
    import requests
    
    resource_id = inputs["resource_id"]
    
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/todos/" + str(resource_id))
        response.raise_for_status()
        
        data = response.json()
        
        if data is None:
            return None
        
        title = data.get("title")
        return title
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error: {e}")