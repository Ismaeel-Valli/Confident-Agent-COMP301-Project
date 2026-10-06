import requests


def solve(inputs):
    """Create a pull request on GitHub using the REST API v2026-03-10."""
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    base = inputs["new_base"]
    body = inputs["new_body"]
    draft = inputs["new_draft"]
    head = inputs["new_head"]
    title = inputs["new_title"]
    credential = inputs["credential"]

    url = "https://api.github.com/repos/{owner}/{repo}/pulls".format(
        owner=owner, repo=repo
    )

    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
    }

    payload = {
        "title": title,
        "body": body,
        "head": head,
        "base": base,
        "draft": draft,
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    if response.status_code == 201:
        return None

    return response.json()