from login import login_page
from flask import Flask
from config import config, BaseConfig
from index import index_page
from exec import file_exec
from files import current_file
from flask_cors import CORS
from model import db


def create_app(config_name: BaseConfig = config['default']):
    flask_app = Flask(__name__)
    CORS(flask_app, supports_credentials=True)
    flask_app.config.from_object(config_name)
    db.init_app(flask_app)
    flask_app.register_blueprint(login_page)
    flask_app.register_blueprint(index_page)
    flask_app.register_blueprint(file_exec)
    flask_app.register_blueprint(current_file)
    return flask_app


if __name__ == '__main__':
    app = create_app()
    if not db.engine.has_table('users'):
        db.createAll()
    app.run(host='0.0.0.0', debug=True)
