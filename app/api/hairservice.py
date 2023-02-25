from app.database.model import Users, Services, service_schema, services_schemas
from flask import request, make_response, jsonify
from app import app, db
import logging
from app.utils.responses import m_return
import app.utils.responses as resp
from app.utils.decorators import permission
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@app.route('/stylings', method=['POST'])
@jwt_required()
def create_services():
    
    data = request.get_json()
    
    try:
        style = data['style']
        description = data['description']
        cost = data['cost']
        duration = data['duration']
        user_id = get_jwt_identity()
        
    except Exception as why:
        
        logging.warning(why)
        
        return m_return(http_code=resp.MISSED_PARAMETERS['http_code'], message=resp.MISSED_PARAMETERS['message'],
                        code=resp.MISSED_PARAMETERS['code'])
        
    service = Services(style=style, description=description, cost=cost, duration=duration, user_id=user_id)
    
    db.session.add(service)
    db.session.commit()
    
    
    return service_schema.jsonify(service)