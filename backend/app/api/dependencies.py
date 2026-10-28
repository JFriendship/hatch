from fastapi import Request

def get_generator(request: Request):
    return request.app.state.generator

def get_conversation_path(request: Request):
    return request.app.state.conversation_path