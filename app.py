from flask import Flask
from flask_smorest import Api

from db import db

import models
import os

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

# highlight-start
def create_app(db_url=None):
    # highlight-end
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # highlight-start
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    # highlight-end
    api = Api(app)

    # highlight-start
    with app.app_context():
        db.create_all()
    # highlight-end

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app