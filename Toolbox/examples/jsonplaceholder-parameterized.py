import requests

def get_title(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()["title"]
