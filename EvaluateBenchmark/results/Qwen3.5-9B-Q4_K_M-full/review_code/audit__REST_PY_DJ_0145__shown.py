import requests

def solve(inputs):
    base_url = "https://dummyjson.com/users/add"
    
    payload = {
        "firstName": inputs["new_firstName"],
        "username": inputs["new_username"]
    }
    
    try:
        response = requests.post(base_url, json=payload)
        response.raise_for_status()
        
        if response.status_code == 201:
            data = response.json()
            return data.get('id')
        elif response.status_code == 200:
            return None
        else:
            raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")