from app.database.model import Users, user_schema, users_schema, service_schema,services_schemas, Services
from flask import request, make_response, jsonify
from app import app, db
import logging
import json
import app.utils.responses as resp
from app.utils.responses import m_return 
from app.utils.decorators import permission
from flask_jwt_extended import create_access_token, create_refresh_token ,jwt_required, get_jwt_identity,decode_token

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/stylings', methods=['POST'])
@jwt_required()
@permission(2)
def add_style():
        
    data = request.get_json()
    email = get_jwt_identity()
    user_id= Users.query.filter_by(email=email).first()
    
    
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
      
    service = Services(style=style, description=description, cost=cost, duration=duration, user_id=user_id.id)
    
    
    db.session.add(service)
    db.session.commit()
    
    
    return service_schema.jsonify(service), 201

@app.route('/stylings', methods=['GET'])
def get_styles():
    
    my_styles = Services.query.all()
    
    return services_schemas.jsonify(my_styles)

@app.route('/stylings/<int:id>', methods=['GET'])
def one_styles(id):
    
    my_style = Services.query.get_or_404(id)
    
    return service_schema.jsonify(my_style)

@app.route('/stylings/<int:id>', methods=['PUT'])
@permission(2)
def update_style(id):
    
    
    my_style = Services.query.get_or_404(id)
    
    data = request.get_json()
    
    style = data['style']
    description = data['description']
    cost = data['cost']
    duration = data['duration']
    
    my_style.style = style
    my_style.description = description
    my_style.cost = cost
    my_style.duration = duration
    
    db.session.commit()
    
    return service_schema.jsonify(my_style), 200


    
@app.route('/stylings/<int:id>', methods=['DELETE'])
@permission(2)
def delete_style(id):
     
    my_style = Services.query.get_or_404(id)
     
    if not my_style:
         
        return make_response(jsonify({
        "status": 404,
        "error": "No style found with that id"
     }), 404)
     
    db.session.delete(my_style)
    db.session.commit()
     
    return jsonify({'message': 'deleted successfully'})
 
     
    