from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.restful import Resource, Api
from flask.ext.bcrypt import Bcrypt


def initialize_api(app, api):
	resources = getattr(app, 'api_registry', None)
	if resources and isinstance(resources, (list, tuple)):
		for resource, args, kwargs in resources:
			api.add_resource(resource, *args, **kwargs)

def create_app(app_name, config):
	
	app = Flask(app_name)
	app.config.from_object(config)

	app.db = SQLAlchemy(app)

	app.migrate = Migrate(app,app.db)

	app.bcrypt = Bcrypt(app)

	app.api = Api(app, prefix='/api/v1')

	app.api_registry = []

	return app


