import requests


def solve(inputs):
    """Add a new pet to the Swagger Petstore API."""
    base_url = "https://petstore3.swagger.io"
    endpoint = "/api/v3/pet"
    
    # Build the payload from inputs
    payload = {
        "category": inputs["new_category"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "status": inputs["new_status"]
    }
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            base_url + endpoint,
            json=payload,
            headers=headers
        )
        
        # Raise exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Return the name value if present, otherwise None
        data = response.json()
        return data.get("name")
    
    except requests.exceptions.HTTPError as e:
        raise e
    except requests.exceptions.RequestException as e:
        raise e