import requests

def get_title(url: str) -> str | None:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json().get("title")
