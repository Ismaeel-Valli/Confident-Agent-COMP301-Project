def solve(inputs):
    import requests
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/albums"
    headers = {"Content-Type": "application/json"}
    payload = {"title": inputs["new_title"]}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 201:
        raise Exception(f"Failed to create album: {response.status_code} {response.text}")
    data = response.json()
    return data.get("title")