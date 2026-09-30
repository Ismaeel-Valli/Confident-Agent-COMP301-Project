def solve(inputs):
    """
    Retrieve one page of products from DummyJSON with pagination and field filtering.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip (for pagination).
            - included_fields (str): Comma-separated list of fields to include in the response.
    
    Returns:
        dict or None: Decoded JSON response containing the requested products, or None if empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not 200).
    """
    import requests
    
    base_url = "https://dummyjson.com/products"
    params = {
        "skip": inputs["results_to_skip"],
        "limit": inputs["result_limit"]
    }
    
    # Parse included_fields as a comma-separated list
    fields_list = [f.strip() for f in inputs["included_fields"].split(",")]
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    # Filter the products to include only the requested fields
    filtered_products = []
    for product in data.get("products", []):
        filtered_product = {}
        for field in fields_list:
            if field in product:
                filtered_product[field] = product[field]
        filtered_products.append(filtered_product)
    
    # Construct the response with only the requested fields
    filtered_response = {
        "products": filtered_products,
        "total": data.get("total", 0),
        "skip": data.get("skip", inputs["results_to_skip"]),
        "limit": data.get("limit", inputs["result_limit"]),
        "total_count": data.get("total_count", 0)
    }
    
    return filtered_response if filtered_products else None