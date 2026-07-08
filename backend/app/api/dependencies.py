from fastapi import Request

def get_generator(request: Request):
    return request.app.state.generator