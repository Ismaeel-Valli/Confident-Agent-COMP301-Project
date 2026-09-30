import requests

def solve(inputs):
    base_url = "https://dummyjson.com/products"
    params = {
        "limit": inputs["result_limit"],
        "sort": inputs["sort_field"]
    }
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")
    return response.json()