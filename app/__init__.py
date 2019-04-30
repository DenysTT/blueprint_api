from flask import Flask
from flask_mongoengine import MongoEngine
from app.blueprints.api import api
import os


def create_app(test_config=None):
    app = Flask(__name__)

    app.config['MONGODB_HOST'] = os.getenv('MONGO_HOST', 'localhost')
    app.config['MONGODB_PORT'] = os.getenv('MONGODB_PORT', 27017)
    if test_config is None:
        app.config['MONGODB_DB'] = os.getenv('MONGO_DB', 'revolut_api')
    else:
        # load the test config if passed in
        app.config.update(test_config)

    db = MongoEngine(app)

    app.register_blueprint(api)
    return app
