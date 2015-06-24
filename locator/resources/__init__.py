from flask.ext.restful import Resource, fields, marshal, abort
from flask import make_response, request
from locator import app, api, logger
import json
from werkzeug.exceptions import HTTPException
from locator.core.utilities import DateJSONEncoder

class ValidationFailed(HTTPException):
	"""
	*34* `Validation Failed`
	Custom exception thrown when form validation fails.
	This is only useful when making REST api calls
	"""
	name = "Validation Failed"
	code = 34
	description = (
		'<p>Validation Failed</p>'
	)

	def __init__(self, data, description=None):
		"""
		param: data: A dictionary containing the field errors that occured
		param: description: Optional description to send through
		"""
		HTTPException.__init__(self)
		self.data = data


class IntegrityException(HTTPException):
	"""
	*32* `Integrity Exception`
	Custom exception thrown when an attempt to save a resource fails.
	This is only useful when making REST api calls
	"""
	name = "Integrity Exception"
	code = 32
	description = (
		'<p>Integrity Exception</p>'
	)

	def __init__(self, e):
		"""
		param: e: parent exception to wrap and manipulate
		"""
		HTTPException.__init__(self)
		self.data = {"name": self.name}
		bits = e.message.split("\n")
		if len(bits) > 1:
			self.data["error"] = bits[0]
			self.data["message"] = " ".join(bits[1:]).strip()
		else:
			self.data["message"] = " ".join(bits).strip()


	def get_response(self, environment):
		resp = super(IntegrityException, self).get_response(environment)
		resp.status = "%s %s" (self.code, self.name.upper())
		return resp


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data, cls=DateJSONEncoder), code)
    resp.headers.extend(headers or {})
    return resp

# @app.errorhandler(34)
# def form_validation_error(error):
# 	""" Error handler for custom form validation errors """
# 	logger.info(error)
# 	return api.make_response(error.data, error.status)


class BaseResource(Resource):

	validation_form = None
	resource_fields = None
	resource_name = None

	@property
	def output_fields(self):
		return {
			'id': fields.Integer,
			'date_created': fields.DateTime(dt_format='rfc822'),
			'last_updated': fields.DateTime(dt_format='rfc822')
		}

	def object(self, id):
		pass

	def prepare_errors(self, data): 

		errors = {}

		for key, value in data.items():
			_res = [str(item) for item in value]
			errors[str(key)] = _res

		return errors

	def adjust_form_fields(self, form):
		return form

	def validate_form(self, form, obj=None, adjust_fxn=None):
		
		if form is None:
			abort(405)

		f = form(obj=obj, csrf_enabled=False)

		if adjust_fxn:
			adjust_fxn(f)

		if f.validate():
			return f.data, request.files

		else:
			raise ValidationFailed(data=self.prepare_errors(data=f.errors))

	def save(self, attrs, files=None):
		abort(405)

	def get(self):
		if self.model_class:
			query = self.model_class.query.all()
			return {'query': [c.as_dict() for c in query]}

		else:
			abort(405, message='Method not allowed')

	def post(self):
		
		attrs, files = self.validate_form(form=self.validation_form, adjust_fxn=self.adjust_form_fields)

		try:
			obj = self.save(attrs, files)
			output_fields = self.output_fields
			output_fields.update(self.resource_fields or {})	
			return marshal(obj, output_fields), 201	
		except Exception, error:
			raise IntegrityException(error)


class AppBaseResource(BaseResource):

	def get(self, id, resource_name=None):

		if resource_name:
			query_method = getattr(self, '%s_query_method' %resource_name, None)
			resource_fields = getattr(self, '%s_resource_fields' %resource_name, None)
			model_class = getattr(self, '%s_model_class' %resource_name, None)
			
			if not query_method or not model_class:
				abort(404)

		else:
			obj = self.model_class.query.get_or_404(id)
			output_fields = self.output_fields
			output_fields.update(self.resource_fields or {})
			return marshal(obj, output_fields), 201

	def post(self, id, resource_name=None):

		_obj = self.model_class.query.get_or_404(id)

		if not resource_name:
			return self.put(id, resource_name)

		post_method = getattr(self, 'post_%s' %resource_name, None)
		adjust_form_fields = getattr(self, '%s_adjust_form_fields' %resource_name, None)
		validation_form = getattr(self, '%s_validation_form' %resource_name, None)
		resource_fields = getattr(self, '%s_resource_fields' %resource_name, None)

		if not post_method:
			abort(405)

		attrs, files = self.validate_form(validate_form, obj=_obj, adjust_fxn=adjust_form_fields)

		try:
			obj = post_method(id, attrs, files)
			output_fields = self.output_fields
			output_fields.update(self.resource_fields or {})	
			return marshal(obj, output_fields), 200
		except Exception, error:
			raise IntegrityException(error)


	def put(self, id, resource_name=None):

		_obj = self.model_class.query.get_or_404(id)
		output_fields = self.output_fields
		output_fields.update(self.resource_fields or {})

		if not resource_name:
			attrs, files = self.validate_form(self.validation_form, obj=_obj, adjust_fxn=self.adjust_form_fields)

			try:
				obj = self.update(id, attrs, files)

			except Exception, e:
				raise IntegrityException(e)
		else:
			validation_form = getattr(self, '%s_validation_form' %resource_name, None)
			adjust_form_fields = getattr(self, '%s_adjust_form_fields' %resource_name, None)
			do_method = getattr(self, 'do_%s' %resource_name, None)

			if not do_method:
				abort(405)

			attrs, files = self.validate_form(validation_form, obj=_obj, adjust_fxn=adjust_form_fields)

			try:
				obj = do_method(id, attrs, files)
			except Exception, error:
				raise IntegrityException(error)
		return marshal(obj, output_fields), 200

	def delete(self, id, resource_name=None):

		obj = self.model_class.query.get_or_404(id)

		if resource_name:
			abort(405)

		try:
			self.destroy(id)

			return '', 201
		except Exception, e:
			raise IntegrityException(e)







