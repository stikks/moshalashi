from flask import current_app as app

db = app.db

migrate = app.migrate

api = app.api

bcrypt = app.bcrypt

logger = app.logger

def register_api(resource, *args, **kwargs):
	kwargs["endpoint"] = getattr(resource, 'resource_name', kwargs.get("endpoint", None))
	return app.api_registry.append((resource,  args, kwargs))