from app.database.model import user_schema, users_schema, service_schema,services_schemas, Services
from flask import request, make_response, jsonify
from app import app, db
import logging
from app.auth.model import User
from app.utils.services import Query
from app.service.model import ServiceModel
import json
import app.utils.responses as resp
from app.utils.responses import m_return 
from app.utils.decorators import permission
from flask_jwt_extended import jwt_required, get_jwt_identity



@app.route('/stylings', methods=['POST'])
@jwt_required()
@permission(2)
def add_style():
        
    data = request.get_json()
    email = get_jwt_identity()
    user_id= User.query.filter_by(email=email).first()
    
    
    try:
        style = data['style']
        description = data['description']
        cost = data['cost']
        duration = data['duration']
        user_id = user_id
        
        
        
    except Exception as why:
        
        logging.warning(why)
        
        return m_return(http_code=resp.MISSED_PARAMETERS['http_code'], message=resp.MISSED_PARAMETERS['message'],
                        code=resp.MISSED_PARAMETERS['code'])
      
    service = ServiceModel.create_service(style=style, description=description, cost=cost, duration=duration, user_id=user_id.id)
    
    return service_schema.jsonify(service), 201

@app.route('/stylings', methods=['GET'])
def get_styles():
    
    my_styles = Query.get_all(Services)
    
    return services_schemas.jsonify(my_styles)

@app.route('/stylings/<int:id>', methods=['GET'])
def one_styles(id):
    
    my_style = Query.get_one(id, Services)
    
    return my_style

@app.route('/stylings/<int:id>', methods=['PUT'])
@permission(2)
def update_style(id):
    
    data = request.get_json()
    
    style = data['style']
    description = data['description']
    cost = data['cost']
    duration = data['duration']
    
    my_style = ServiceModel.update(id, style=style, description=description, cost=cost, duration=duration)
    
    return service_schema.jsonify(my_style), 200


    
@app.route('/stylings/<int:id>', methods=['DELETE'])
@permission(2)
def delete_style(id):
     
    service = Services.query.filter_by(id=id).first()
        
    if not service:
        return m_return(http_code=resp.NOT_FOUND_404['http_code'],
                    message=resp.NOT_FOUND_404['message'],
                    code=resp.NOT_FOUND_404['code'])
     
    ServiceModel.delete(service)
    
    return m_return(http_code=resp.DELETED_SUCCESS['http_code'],
                    message=resp.DELETED_SUCCESS['message'],
                    code=resp.DELETED_SUCCESS['code'])
        

 
     
    