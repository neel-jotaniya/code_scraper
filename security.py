import functools
from model import User, db
from flask import request

def is_valid(api_key):
    return api_key == "123"
def api_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if request.json and "api_key" in request.json:
            api_key = request.json.get("api_key")
        else:
            return {"message": "Please provide an API key"}, 400
        if request.method == "POST" and is_valid(api_key):
            return func(*args, **kwargs)
        else:
            return {"message": "The provided API key is not valid"}, 403
    return decorator