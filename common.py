from fastapi import Request


def is_test_request(request: Request) -> bool:
    return "test" not in request.query_params or not request.query_params["test"]
