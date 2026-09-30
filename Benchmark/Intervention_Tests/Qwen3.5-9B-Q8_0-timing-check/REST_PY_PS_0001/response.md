### Confidence Agent Report

**Decision:** deliver
**EWCS:** 0.85 (signed: 0.85, applicable weight: 14)

| Layer | State | Tier | Weight | Factor | Positive | Signed |
|---|---|---|---|---|---|---|
| interface | verified_correct | tier_2 | 3 | 0.8 | 2.4 | 2.4 |
| identifier | verified_correct | tier_4 | 3 | 0.5 | 1.5 | 1.5 |
| access_point | verified_correct | tier_1 | 4 | 1 | 4 | 4 |
| input_contract | verified_correct | tier_1 | 2 | 1 | 2 | 2 |
| output_contract | not_applicable | none | 1 | 0 | 0 | 0 |
| contextual | verified_correct | tier_1 | 2 | 1 | 2 | 2 |

Scope: API-claim and static evidence only. EWCS is not a probability of correctness. Task behavior has not been independently checked by this verifier.

Policy 2026-09-25.1: thresholds 0.85/0.6, uncertainty gate on.

Evidence:

- interface: requests maps to requests (2.34.2). Installation/callables checked separately by Pyright.
- identifier: No identifier, attribute or API-call diagnostics in the configured environment (Pyright standard mode). A clean check does not establish REST contracts or task behavior.
- access_point: PUT https://petstore3.swagger.io/api/v3/pet matches the declared server and operation PUT /pet.
- input_contract: Required inputs, locations and supported value constraints checked for call_36_15 (/pet). Noncritical: body.id: runtime value inputs['new_resource_id'] is not statically known; its value constraints are not checked; body.name: runtime value inputs['new_name'] is not statically known; its value constraints are not checked; body.photoUrls: runtime value inputs['new_photo_links'] is not statically known; its value constraints are not checked
- output_contract: No tracked response-field accesses.
- contextual: Required authentication placement and static shape match one security alternative. Credential validity is not tested. Noncritical: required scopes (write:pets, read:pets) belong to the petstore_auth token and cannot be checked statically; the credential is assumed to carry them; the oauth2 Bearer token credential is a runtime value; its validity is not tested

```python
import requests


def solve(inputs):
    """
    Update an existing pet in the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Must contain:
            - new_resource_id (int): The id value for the updated pet.
            - new_name (str): The name value for the updated pet.
            - new_photo_links (list of str): The photoUrls value for the updated pet.
            - credential (str): Bearer token for authentication.
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
    
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://petstore3.swagger.io"
    endpoint = "/api/v3/pet"
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"]
    }
    
    response = requests.put(url, json=payload, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    if len(response.content) == 0:
        return None
    
    return response.json()
```