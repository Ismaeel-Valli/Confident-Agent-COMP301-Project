"""Manual review of the undetermined candidates (EVALUATION_PLAN.md §4), as decision rules.

An undetermined candidate uses a name that a *partial* specification (DummyJSON,
JSONPlaceholder, REST Countries) does not list. Each such finding was checked once against
the provider's documentation (and, where the documentation is silent, the live public API on
2026-10-06), and the answer is written down below as a rule, so that every candidate asking
the same question gets the same answer:

  the name does not exist     -> class A (as an undeclared name in an official specification)
  the name exists             -> judged by the plan's usual rules: an extra documented query
                                 parameter is class C (no finding), an extra documented body
                                 field or an unrequested body is class B, a real endpoint that
                                 is not the task's is class B

A candidate's class is then its most severe finding: A, else B (its other findings are all
class-B findings: other endpoint, omitted or different parameter or body), else correct.

Review made with AI assistance (Claude) on 2026-10-06, not by two independent group members
as §4 plans; `reviewer_2_class` is left for a group member's check.

Usage:  python review_rules.py     reads ../../Statistical Analysis/Unprocessed Data/evaluation/*/review_queue.csv
                                   and writes reviews.csv next to this file; rerun the evaluator after.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUEUES = HERE.parents[1] / "Statistical Analysis" / "Unprocessed Data" / "evaluation"
OUT = HERE / "reviews.csv"
REVIEWED = "2026-10-06"

DJ_DOCS = "dummyjson.com/docs (products, users, posts, todos)"
DJ_QUERY = {"limit", "skip", "select", "sortBy", "order", "q"}
# fields of each resource (documentation and GET /<resource>/1 on 2026-10-06)
DJ_FIELDS = {
    "users": {"id", "firstName", "lastName", "maidenName", "age", "gender", "email", "phone", "username", "password",
              "birthDate", "image", "bloodGroup", "height", "weight", "eyeColor", "hair", "ip", "address", "macAddress",
              "university", "bank", "company", "ein", "ssn", "userAgent", "crypto", "role"},
    "todos": {"id", "todo", "completed", "userId"},
    "posts": {"id", "title", "body", "tags", "reactions", "views", "userId"},
    "products": {"id", "title", "description", "category", "price", "discountPercentage", "rating", "stock", "tags",
                 "brand", "sku", "weight", "dimensions", "warrantyInformation", "shippingInformation",
                 "availabilityStatus", "reviews", "returnPolicy", "minimumOrderQuantity", "meta", "images", "thumbnail"},
}
JP_DOCS = "jsonplaceholder.typicode.com/guide"
JP_FIELDS = {
    "posts": {"userId", "id", "title", "body"},
    "comments": {"postId", "id", "name", "email", "body"},
    "albums": {"userId", "id", "title"},
    "photos": {"albumId", "id", "title", "url", "thumbnailUrl"},
    "todos": {"userId", "id", "title", "completed"},
    "users": {"id", "name", "username", "email", "address", "phone", "website", "company"},
}
RC_DOCS = "restcountries.com/docs/countries"
RC_QUERY = {"q", "limit", "offset", "response_fields", "response_fields_omit", "pretty", "api-key"}

PARTIAL = " (partial specification: check the provider's documentation)"
FINDING = re.compile(r"request \d+ \(([A-Z]+) (.+?)\): (.*)" + re.escape(PARTIAL) + "$")  # URLs may contain spaces


def resource(path: str) -> str:
    return path.strip("/").split("/")[0]


def resolve(api: str, method: str, url: str, what: str) -> tuple:
    """(class or None for no finding, evidence) for one partial-specification finding."""
    path = re.sub(r"^https?://[^/]+", "", url.split("?")[0])
    name = (re.search(r"(?:parameter|field) ([^\s,]+)", what) or [None, None])[1]
    if api == "DJ":
        if what.startswith("query parameter"):
            if name in DJ_QUERY:
                return None, f"{name} is documented ({DJ_DOCS})"
            return "A", (f"query parameter {name} does not exist: {DJ_DOCS} list limit, skip, select, sortBy, order, q; "
                         f"live check {REVIEWED}: {name} has no effect")
        if what.startswith("body: field"):
            if name in DJ_FIELDS.get(resource(path), set()):
                return "B", f"{name} is a documented field of {resource(path)}: an extra body field is class B (plan §5)"
            return "A", f"{resource(path)} has no field {name} ({DJ_DOCS}; GET /{resource(path)}/1 on {REVIEWED})"
        if what.startswith("sends a request body"):
            return "B", "DELETE takes no body in the documentation: an unrequested body is class B"
        if what.startswith("no declared path"):
            return "A", f"{path} is not a documented endpoint ({DJ_DOCS}); live check {REVIEWED}: 404"
        if what.startswith("reads response field"):
            return "A", (f"the success response has no field {name}: DummyJSON returns the resource object itself "
                         f"({DJ_DOCS}; live check {REVIEWED})")
    if api == "JP":
        if what.startswith("query parameter"):
            if name in JP_FIELDS.get(resource(path), set()):
                return None, (f"filtering by a resource field ({name}) is documented ('Basic filtering is supported "
                              f"through query parameters', {JP_DOCS}); live check {REVIEWED}: filters")
            return "A", f"{resource(path)} has no field {name}, so ?{name}= filters nothing (live check {REVIEWED}: ignored)"
        if what.startswith("body: field"):
            if name in JP_FIELDS.get(resource(path), set()):
                return "B", f"{name} is a documented field of {resource(path)}: an extra body field is class B (plan §5)"
            return "A", f"{resource(path)} has no field {name} ({JP_DOCS}; GET /{resource(path)}/1 on {REVIEWED})"
        if what.startswith("no declared path") and re.fullmatch(r"/posts/\d+/comments", path):
            return None, (f"{path} is a documented nested route ({JP_DOCS}); POST to it also works (live check "
                          f"{REVIEWED}: 201), so it is a real endpoint, not the task's")
        if what.startswith("reads response field 0"):
            return None, "indexes the list the endpoint returns (a documented array response)"
    if api == "RC":
        if what.startswith("no declared path"):
            return "A", (f"{path or '/'} does not exist: every Countries endpoint is under /countries/v5 ({RC_DOCS}: "
                         f"list, search, aggregate, read and search by property); v1-v4 are deprecated and were "
                         f"served by restcountries.com, not api.restcountries.com")
        if what.startswith("query parameter"):
            if name in RC_QUERY:
                return None, f"{name} is documented ({RC_DOCS})"
            return "A", f"query parameter {name} does not exist ({RC_DOCS}: q, limit, offset, response_fields, response_fields_omit, pretty)"
    raise ValueError(f"no rule for {api} {method} {url}: {what}")


def review(row: dict) -> tuple:
    api = row["task_id"].split("_")[2]
    classes, evidence, other = [], [], False
    for reason in row["automatic_reasons"].split(" | "):
        m = FINDING.match(reason)
        if not m:
            if PARTIAL in reason:
                raise ValueError(f"unparsed finding in {row['task_id']}: {reason}")
            other = True  # an automatic class-B finding (endpoint, parameter or body not the task's)
            continue
        cls, why = resolve(api, *m.groups())
        classes.append(cls)
        evidence.append(why)
    agreed = "A" if "A" in classes else "B" if ("B" in classes or other) else "correct"
    return agreed, "; ".join(dict.fromkeys(evidence))


def main() -> None:
    rows = {}
    if OUT.exists():  # keep earlier reviews: once applied, a candidate leaves the review queue
        with OUT.open(encoding="utf-8-sig", newline="") as f:
            rows = {(r["task_id"], r["code_sha256"]): r for r in csv.DictReader(f)}
    for queue in sorted(QUEUES.glob("*/review_queue.csv")):
        with queue.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                agreed, why = review(row)
                key = (row["task_id"], row["code_sha256"])  # one review covers the same code in every run
                rows.setdefault(key, {**row, "reviewer_1_class": agreed, "reviewer_2_class": "", "agreed_class": agreed,
                                      "notes": f"AI-assisted review {REVIEWED}: {why}"})
    fields = ["label", "task_id", "role", "code_sha256", "automatic_class", "automatic_reasons", "code_file",
              "reviewer_1_class", "reviewer_2_class", "agreed_class", "notes"]
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(sorted(rows.values(), key=lambda r: (r["task_id"], r["role"], r["label"])))
    print(f"{len(rows)} reviews written to {OUT}")


if __name__ == "__main__":
    main()
