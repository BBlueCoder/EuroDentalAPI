from starlette.requests import Request

def generate_the_address(req : Request, extra_path : str):
    if req.url.port:
        return f"{req.url.scheme}://{req.url.hostname}:{req.url.port}{extra_path}"
    return f"{req.url.scheme}://{req.url.hostname}{extra_path}"