def solve(inputs):
    import requests
    
    base_url = "https://jsonplaceholder.typicode.com"
    
    # Create a new todo with only the provided fields
    response = requests.post(
        f"{base_url}/todos",
        json={
            "title": inputs["new_title"],
            "body": "",  # Required field, but not provided in inputs; using empty string
            "userId": 1   # Required field, but not provided in inputs; assuming a default user ID
        }
    )
    
    if response.status_code != 201:
        raise Exception(f"Failed to create todo: {response.status_code} - {response.text}")
    
    return response.json()["id"]