import requests

def solve(inputs):
    url = "https://restcountries.com/v5.1/all"
    headers = {"Authorization": f"Bearer {inputs['credential']}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    data = response.json()
    return data if data else None