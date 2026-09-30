import requests

def solve(inputs):
    post_id = inputs["post_identifier"]
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    data = response.json()
    return data if data else None