# app/auth.py
import os
from flask import request

def authenticate_request(req):
    """Verify if the incoming request is authorized."""
    try:
        chat_id = req.json['message']['chat']['id']
        allowed_id = os.getenv('ALLOWED_USER_ID')
        return str(chat_id) == allowed_id
    except KeyError:
        return False
