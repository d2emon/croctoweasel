errors = (
    {"errcode": 0, "error": "No error"},
    {"errcode": 1, "error": "Wrong action"},
    {"errcode": 2, "error": "Unknown error"},
)


def jsoned(errorcode):
    import json

    return json.dumps(errors[errorcode]).encode("UTF-8")
