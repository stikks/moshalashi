# from locator.resources import BaseResource
from flask.ext.restful import fields, Resource, abort
from locator.forms import *
from locator.services.auth import authenticate_user, create_user, delete_user, update_user
from locator.services import mosque
from locator import register_api, app, logger
from locator.models import *
from flask.ext.restful import reqparse
from locator.resources import BaseResource, AppBaseResource, ValidationFailed

class LoginResource(Resource):

	resource_name = 'login'

	def post(self):

		form = LoginForm(csrf_enabled=False)

		if form.validate():
			data = form.data

			user = authenticate_user(**data)

			if user:
				return {'user': user.as_dict()}
			else:
				raise ValidationFailed(data={'password': 'Invalid Password'})
		else:
			raise ValidationFailed(data={'username': 'Invalid Username!'})

class SignUpResource(BaseResource):

	resource_name = 'sign_up'

	validation_form = UserForm

	resource_fields = {
		'username': fields.String,
		'name': fields.String,
		'email': fields.String,
		'gender': fields.String
	}

	def adjust_form_fields(self, form):
		form.country_id.choices = [(c.id, c.name) for c in Country.query.all()]
		form.state_id.choices = [(c.id, c.name) for c in State.query.all()]
		form.sect_id.choices = [(c.id, c.name) for c in Sect.query.all()]
		return form

	def save(self, attrs, files=None):

		user = create_user(**attrs)

		if user:
			return {'user': user.as_dict()}
		else:
			return abort(405, message='Invalid credentials')


class UserResource(AppBaseResource):

	model_class = User

	resource_name = 'user'

	validation_form = UpdateUserForm

	resource_fields = {
		'username': fields.String,
		'name': fields.String,
		'email': fields.String,
		'gender': fields.String
	}

	def update(self, id, attrs, files=None):
		return update_user(id, **attrs)

	def destroy(self, obj_id):
		return delete_user(obj_id)

class MosqueResource(AppBaseResource):

	model_class = Mosque

	resource_name = 'mosque'

	validation_form = MosqueForm

	def post(self):
		logger.info(attrs)

class MapResource(AppBaseResource):

	resource_name = 'map'

	validation_form = MapForm

	def post(self):
		
		form = MapForm(csrf_enabled=False)

		if form.validate():
			mosques = mosque.load_mosques(**form.data)

			if mosques:
				return {'result': mosques}
			else:
				abort(405, message='Invalid request')
		else:
			raise ValidationFailed(data=form.errors)	


class HadithCollection(BaseResource):

	resource_name = 'hadiths'

	model_class = Hadith

	validation_form = HadithForm

	resource_fields = {
		'text': fields.String,
		'source': fields.String,
		'is_verified': fields.Boolean
	}

	def save(self, attrs, files):

		hadith = mosque.create_hadith(**attrs)

		logger.info(hadith)

		if hadith:
			return hadith
		else:
			return abort(405, message='Hadith not created')


class DuaCollection(BaseResource):

	resource_name = 'duas'

	model_class = Dua

	validation_form = DuaForm

	resource_fields = {
		'name': fields.String,
		'text': fields.String,
		'source': fields.String
	}

	def save(self, attrs, files):

		dua = mosque.create_dua(**attrs)

		if dua:
			return dua
		else:
			return abort(405, message='Hadith not created')



register_api(LoginResource, '/login')
register_api(SignUpResource, '/signup')
register_api(UserResource, '/users/<int:id>', '/users/<string:resource_name>')
register_api(MosqueResource, '/mosques/<int:id>', '/mosques/<string:resource_name>')
register_api(MapResource, '/maps')
register_api(HadithCollection, '/hadiths')
register_api(DuaCollection, '/duas')

