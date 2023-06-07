from app.service.model import Services
from flask import request, Blueprint, make_response, jsonify
from app.database.database import db
from app.schemas.schemas import service_schema
from app.service.controllers import ServiceController
import app.utils.responses as resp
from app.utils.responses import m_return 
from app.utils.decorators import permission
from flask_jwt_extended import jwt_required

service_v1 = Blueprint('service_v1', __name__, url_prefix='/api/v1')

@service_v1.route('/stylings', methods=['POST'])
@jwt_required()
@permission(2)
def add_style():
        
    data = request.get_json()
    session = db.session
    
    return ServiceController.create_service(data, session=session)

@service_v1.route('/stylings', methods=['GET'])
def get_styles():
    
    session = db.session
    
    return ServiceController.get_all_services(session=session)

@service_v1.route('/stylings/<int:id>', methods=['GET'])
def one_styles(id):
    
    session = db.session
    
    result = ServiceController.get_service_by_id(id, session=session)
    if result is None:
        return make_response(jsonify({
                "status": 404,
                "message": "service doesn't exist"
            }), 404)
    
    return service_schema.dump(result)

@service_v1.route('/stylings/<int:id>', methods=['PUT'])
@permission(2)
def update_style(id):

    session = db.session
    
    data = request.get_json()
    
    style = data['style']
    description = data['description']
    cost = data['cost']
    duration = data['duration']
    
    my_style = ServiceController.update(id, session=session, style=style, description=description, cost=cost, duration=duration)

    if my_style is None:
        return make_response(jsonify({
                "status": 404,
                "message": "service doesn't exist"
            }), 404)
    
    return service_schema.dump(my_style)


    
@service_v1.route('/stylings/<int:id>', methods=['DELETE'])
@permission(2)
def delete_style(id):
     
    service = Services.query.filter_by(id=id).first()
        
    if not service:
        return m_return(http_code=resp.NOT_FOUND_404['http_code'],
                    message=resp.NOT_FOUND_404['message'],
                    code=resp.NOT_FOUND_404['code'])
     
    ServiceController.delete(service)
    
    return m_return(http_code=resp.DELETED_SUCCESS['http_code'],
                    message=resp.DELETED_SUCCESS['message'],
                    code=resp.DELETED_SUCCESS['code'])
        

 
     
    