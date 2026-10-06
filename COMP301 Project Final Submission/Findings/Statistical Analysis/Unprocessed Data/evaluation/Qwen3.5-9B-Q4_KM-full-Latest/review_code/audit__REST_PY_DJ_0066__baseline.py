import requests

def solve(inputs):
    """
    Updates selected fields of a user via DummyJSON API and returns the response's id value,
    or None if that attribute is absent or the response is empty (successful update).
    Raises an exception for unsuccessful HTTP responses.

    Args:
        inputs (dict): Dictionary containing:
            - resource_id: Identifier of the user to update.
            - new_lastName: New value for the last Name attribute.

    Returns:
        str or None: The 'id' from the response if present, otherwise None.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails (non-2xx status).
    """
    resource_id = inputs.get("resource_id")
    new_lastName = inputs.get("new_lastName")

    # Construct the payload for PATCH request
    payload = {
        "lastName": new_lastName
    }

    # DummyJSON endpoint for updating a user by ID
    url = f"https://dummyjson.com/users/{resource_id}"

    try:
        response = requests.patch(url, json=payload)
        
        # Raise an exception for unsuccessful HTTP responses (non-2xx status codes)
        response.raise_for_status()

        # Check if the response is empty (no content)
        if not response.text.strip():
            return None

        # Parse the JSON response
        data = response.json()

        # Return the 'id' if present, otherwise None
        return data.get("id")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to update user: {e}")