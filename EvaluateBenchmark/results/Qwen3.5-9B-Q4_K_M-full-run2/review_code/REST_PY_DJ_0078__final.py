import requests

def solve(inputs):
    base_url = "https://dummyjson.com/users"
    url = f"{base_url}?newAge={inputs['new_age']}&newFirstName={inputs['new_firstName']}"
    
    response = requests.get(url)
    if response.status_code != 201:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    return response.json()