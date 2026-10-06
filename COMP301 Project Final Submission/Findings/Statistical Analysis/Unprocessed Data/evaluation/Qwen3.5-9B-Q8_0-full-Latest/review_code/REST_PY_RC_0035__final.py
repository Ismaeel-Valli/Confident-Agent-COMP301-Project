import requests

def solve(inputs):
    """
    Search REST Countries v5 by text, skip results, filter attributes.
    
    Args:
        inputs (dict): {
            "results_to_skip": int,
            "included_attributes": list[str],
            "search_text": str,
            "credential": str  # caller-supplied credential
        }
    
    Returns:
        dict or None: Decoded JSON response. None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.restcountries.com/v5"
    params = {
        "search": inputs["search_text"],
        "skip": inputs["results_to_skip"],
        "fields": ",".join(inputs["included_attributes"])
    }
    
    headers = {"Authorization": f"Bearer {inputs['credential']}"}
    
    response = requests.get(f"{base_url}/countries", params=params, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return None if len(data) == 0 else data
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")