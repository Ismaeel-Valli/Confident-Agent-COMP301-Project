def solve(inputs):
    import requests
    
    base_url = "https://dummyjson.com"
    endpoint = "/todos"
    url = f"{base_url}{endpoint}"
    
    params = {
        "limit": inputs["result_limit"],
        "fields": inputs["included_fields"]
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    return data if data else None