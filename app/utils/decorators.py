import functools
import logging

import app.utils.responses as error
from app.utils.auth import jwt
from flask import request

def permission(arg):
    def check_permissions(f):
        
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            
            auth = request.authorization
            
            if auth is None and 'Authorization' in request.headers:
                try:
                    auth_type, token = request.headers['Authorization'].split(None, 1)
                    
                    data = jwt.loads(token)
                    
                    if data['admin'] < arg:
                        
                        return error.NOT_ADMIN
                except ValueError:
                    
                    return error.HEADER_NOT_FOUND
                
                except Exception as why:
                    logging.error(why)
                    
                    return error.INVALID_INPUT_422
            
            return f(*args, **kwargs)
        
        return decorated
    
    return check_permissions