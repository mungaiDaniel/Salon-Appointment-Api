from app import app, db
from app.database.model import Users, Services

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'users': Users, 'services': Services}

if __name__ == '__main__':
    app.debug=True
    app.run(host='127.0.0.1', port=5000)