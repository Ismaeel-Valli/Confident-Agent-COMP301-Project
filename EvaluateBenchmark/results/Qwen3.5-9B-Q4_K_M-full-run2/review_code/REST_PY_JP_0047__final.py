def solve(inputs):
    import requests
    
    user_identifier = inputs["user_identifier"]
    
    url = "https://jsonplaceholder.typicode.com/users/{0}/albums".format(user_identifier)
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data