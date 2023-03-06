from app import db
from app.utils.responses import m_return
import app.utils.responses as resp


class Query:
    
    @staticmethod
    def get_all(table):
        items = db.session.query(table).all() 
        return items
    
    @classmethod
    def get_one(cls, id, table):
        
        service = db.session.query(table).filter_by(id=id).first()
        
        if not service:
            return m_return(http_code=resp.USER_DOES_NOT_EXIST['http_code'],
                        message=resp.USER_DOES_NOT_EXIST['message'],
                        code=resp.USER_DOES_NOT_EXIST['code'])
        
        
        return service