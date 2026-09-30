def solve(inputs):
    """Search REST Countries v5 using caller-supplied credentials."""
    import requests
    
    base_url = "https://api.restcountries.com"
    endpoint = "/v3/search"  # Corrected to v3 based on OpenAPI contract
    
    # Build query parameters
    params = {}
    if inputs.get("result_limit") is not None:
        params["limit"] = inputs["result_limit"]
    if inputs.get("results_to_skip") is not None:
        params["skip"] = inputs["results_to_skip"]
    if inputs.get("search_text") is not None:
        params["searchText"] = inputs["search_text"]
    
    # Build excluded attributes as a comma-separated string
    excluded_attrs = inputs.get("excluded_attributes", [])
    if excluded_attrs:
        params["excludeAttributes"] = ",".join(str(attr) for attr in excluded_attrs)
    
    # Make the request with credentials (assumed to be in headers or body)
    headers = {"Authorization": f"Bearer {inputs['credential']}"}
    
    response = requests.get(f"{base_url}{endpoint}", params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data