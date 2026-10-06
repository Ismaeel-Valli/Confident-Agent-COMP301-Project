import requests

def solve(inputs):
    """
    Looks up countries by an exact match on their common country name using REST Countries v5 API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'value': The exact country name to search for.
            - 'results_to_skip': Number of results to skip (for pagination).
            - 'credential': Caller-supplied credential (e.g., API key or token).
    
    Returns:
        list or None: Decoded JSON response as a list of countries, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (non-2xx status code).
    """
    value = inputs["value"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]

    # REST Countries v5 uses a different endpoint structure. 
    # Exact match on common name can be done via /v5/country/{name} if supported, 
    # but typically the API supports filtering or exact path matching for known names.
    # However, based on standard REST Countries v5 docs, exact name lookup is often:
    # GET https://restcountries.com/v5/name/{name}?fields=...
    # But note: The official v5 API may not support arbitrary name lookups directly without filters.
    # Since the problem states "exact match on their common country name", we assume the endpoint supports it.

    url = f"https://restcountries.com/v5/name/{value}"
    
    headers = {
        "Authorization": f"Bearer {credential}" if credential.startswith("Bearer ") else f"{credential}",
        # If credential is just a key, some APIs expect it in header 'X-API-Key' or similar.
        # But since the problem says "caller-supplied credential", we assume it's meant for auth header.
        # Adjust based on actual API requirement. For REST Countries v5, no auth is typically needed, 
        # but if required, we include it.
    }

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            # If the result is an empty list (no country found), return None as per spec for "successful empty response"
            if not data:
                return None
            # Skip specified number of results if needed (though exact match usually returns 0 or 1)
            skipped_data = data[results_to_skip:] if len(data) > results_to_skip else []
            return skipped_data
        elif response.status_code == 404:
            # Not found is considered unsuccessful in this context? 
            # The problem says "Raise an exception for an unsuccessful HTTP response", so 404 is unsuccessful.
            raise Exception(f"HTTP {response.status_code}: Country not found")
        else:
            raise Exception(f"HTTP {response.status_code}: Unsuccessful response")
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")