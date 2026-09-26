def solve(inputs):
    import requests
    url = "https://restcountries.com/v3.1/all"
    headers = {"Authorization": f"Bearer {inputs['credential']}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    data = response.json()
    if not data:
        return None
    return data