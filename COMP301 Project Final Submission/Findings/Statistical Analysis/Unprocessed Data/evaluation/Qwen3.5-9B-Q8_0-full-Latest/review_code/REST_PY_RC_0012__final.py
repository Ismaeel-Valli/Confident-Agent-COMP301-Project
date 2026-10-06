import requests

def solve(inputs):
    """
    Look up countries by exact match on their two-letter ISO country code using REST Countries v5.
    
    Args:
        inputs (dict): Dictionary containing:
            - value (str): The two-letter ISO country code to match exactly.
            - results_to_skip (int): Number of results to skip.
            - credential (str): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response. Returns None for a successful empty response.
    
    Raises:
        Exception: For an unsuccessful HTTP response.
    """
    base_url = "https://api.restcountries.com"
    country_code = inputs["value"]
    skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    # Construct the API endpoint for exact match by ISO code
    url = f"{base_url}/rest/{country_code}"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # REST Countries v5 returns a list of countries for exact match
        return data if data else None
    elif response.status_code == 404:
        # Country not found
        raise Exception(f"Country code '{country_code}' not found")
    else:
        # Unsuccessful HTTP response
        raise Exception(f"HTTP error {response.status_code}: {response.text}")