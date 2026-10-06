import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - value: The country code to match exactly in borders
            - included_attributes: List of attributes to return
            - credential: Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    """
    base_url = "https://api.restcountries.com"
    value = inputs["value"]
    included_attributes = inputs["included_attributes"]
    credential = inputs["credential"]
    
    # Build query parameters
    params = {
        "border": value,
        "fields": ",".join(included_attributes) if included_attributes else None
    }
    
    # Make the request with credentials in headers
    headers = {"Authorization": f"Bearer {credential}"}
    
    try:
        response = requests.get(f"{base_url}/v5/country", params=params, headers=headers)
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            # REST Countries v5 returns a list of countries
            if not data:
                return None
            return data
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")