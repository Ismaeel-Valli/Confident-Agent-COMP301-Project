import requests

def solve(inputs):
    base_url = "https://dummyjson.com/users/add"
    new_user = {
        "firstName": inputs["new_firstName"],
        "lastName": "Doe",
        "email": f"{inputs['new_firstName'].lower()}@example.com",
        "age": 30,
        "phone": "1234567890",
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zipCode": "10001"
        },
        "image": "https://dummyjson.com/avatar/default"
    }
    
    response = requests.post(base_url, json=new_user)
    if response.status_code != 201:
        raise Exception(f"Failed to create user: {response.status_code} - {response.text}")
    
    return None