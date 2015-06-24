from wtforms import BooleanField, TextField, PasswordField, validators, StringField, IntegerField, SelectField, FloatField, DecimalField
from wtforms.validators import ValidationError, Required, Optional	
from flask_wtf import Form
from locator.models import *
from sqlalchemy import and_, or_

class UserForm(Form):

	name = StringField('Name', validators=[Required()])
	gender = SelectField('Gender', validators=[Optional()], choices=(('male', 'Male'), ('female', 'Female')))
	email = StringField('Email Address', validators=[Required()])
	username = StringField('Username', validators=[Required()])
	password = StringField('Password', validators=[Required()])
	verify_password = StringField('Verify Password', validators=[Required()])
	country_id = SelectField('Country', coerce=int,  validators=[Required()])
	sect_id = SelectField('Sect', coerce=int,  validators=[Optional()])
	state_id = SelectField('Country', coerce=int,  validators=[Optional()])

	def validate_verify_password(form, field):

		if field.data != form.password.data:
			raise ValidationError('Passwords do not match')

	def validate_username(form, field):

		user = User.query.filter(or_(User.email==form.email.data, User.username==field.data)).first()

		if user:
			raise ValidationError('Username already exists, pick another!')


class LoginForm(Form):

	username = StringField('Username', validators=[Required()])
	password = StringField('Password', validators=[Required()])

	def validate_username(form, field):

		user = User.query.filter(User.username==field.data).first()

		if not user:
			raise ValidationError('Inavlid Username!')

class MosqueForm(Form):

	name = StringField('Name', validators=[Required()])
	address = StringField('Address', validators=[Required()])
	gps_location = StringField('GPS', validators=[Required()])
	user_id = IntegerField('User ID', validators=[Optional()])
	sect_id = IntegerField('Sect ID', validators=[Optional()])

class MapForm(Form):

	latitude = DecimalField('Latitude', validators=[Required()])
	longitude = DecimalField('Longitude', validators=[Required()])


class UpdateUserForm(Form):

	id = IntegerField('ID', validators=[Required()])
	name = StringField('Name', validators=[Required()])
	gender = SelectField('Gender', validators=[Optional()], choices=(('male', 'Male'), ('female', 'Female')))
	country_id = SelectField('Country', coerce=int,  validators=[Required()])
	sect_id = SelectField('Sect', coerce=int,  validators=[Optional()])
	state_id = SelectField('Country', coerce=int,  validators=[Optional()])

class HadithForm(Form):

	source = StringField('Source', validators=[Required()])
	text = TextField('Description', validators=[Required()])
	user_id = IntegerField('USer ID', validators=[Required()])

class DuaForm(Form):

	name = StringField('Name', validators=[Optional()])
	text = TextField('Description', validators=[Required()])
	source = StringField('Source', validators=[Optional()])
	user_id = IntegerField('USer ID', validators=[Required()])