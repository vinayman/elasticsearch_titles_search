from flask import Flask, jsonify
from dashboard import jinja_filters

from dashboard.blueprints.dashboard.blueprint import dashboard as dashboard_blueprint
from dashboard.blueprints.titles.blueprint import titles as titles_blueprint
from dashboard.blueprints.titles.errors import BadRequest


def create_app():
    app = Flask(__name__)
    register_jinja_filters(app)
    register_blueprints(app)
    register_errors(app)
    return app


def register_jinja_filters(app):
    app.jinja_env.filters["commify"] = jinja_filters.commify
    app.jinja_env.filters["typed_value"] = jinja_filters.typed_value


def register_blueprints(app):
    app.register_blueprint(dashboard_blueprint, url_prefix="/")
    app.register_blueprint(titles_blueprint, url_prefix="/titles")


def register_errors(app):
    def handle_bad_request(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    app.register_error_handler(BadRequest, handle_bad_request)
