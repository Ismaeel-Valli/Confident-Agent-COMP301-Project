import requests

def solve(inputs):
    """Retrieve posts from JSONPlaceholder and return decoded JSON response."""
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = "/posts"
    
    url = f"{base_url}{endpoint}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            return data if data else None
        else:
            raise Exception(f"Unexpected status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")