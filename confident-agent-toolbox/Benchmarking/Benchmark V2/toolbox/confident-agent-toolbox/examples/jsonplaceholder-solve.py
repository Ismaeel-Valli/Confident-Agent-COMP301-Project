"""Development reference for the pilot task; no request runs on import."""
import requests


def solve(inputs):
    response = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=10)
    response.raise_for_status()
    if not 200 <= response.status_code < 300:
        raise requests.HTTPError(f"Unsuccessful HTTP response: {response.status_code}", response=response)
    if not response.content:
        return None
    return response.json()
