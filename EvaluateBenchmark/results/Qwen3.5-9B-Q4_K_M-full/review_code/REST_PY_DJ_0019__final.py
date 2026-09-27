def solve(inputs):
    import requests
    base_url = inputs.get("base_url", "https://dummyjson.com")
    todos_page = inputs.get("todos_page", 1)
    
    url = f"{base_url}/todos?page={todos_page}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data.get("todos"):
        return None
    
    return data