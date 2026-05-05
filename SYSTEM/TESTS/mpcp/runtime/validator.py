REQUIRED_FIELDS = ["TASK", "SCOPE", "INCLUDE", "EXCLUDE", "MODEW", "OUTPUT"]


def validate_paper(data):
    # missing required
    for field in REQUIRED_FIELDS:
        if field not in data or not data[field]:
            return False, f"MISSING:{field}"

    # include / exclude must not overlap
    include = set(data["INCLUDE"].split(","))
    exclude = set(data["EXCLUDE"].split(","))

    if include & exclude:
        return False, "CONFLICT:INCLUDE_EXCLUDE"

    # scope sanity
    if data["SCOPE"] == "*":
        return False, "INVALID:SCOPE_TOO_BROAD"

    return True, "OK"
