from locator import app,db, logger
from locator.models import *
from locator.core.utilities import populate_object, clean_dict
from sqlalchemy import and_, or_

ignored_args = ['id', 'date_created', 'last_updated']

def authenticate_user(username, password, **kwargs):

	user = User.query.filter(func.lower(User.username)==username.lower()).first()

	if not user:
		return None

	if user and user.check_password(password):
		return user
	else:
		return None


def create_user(username, name, email, password, country_id, gender=None, state_id=None, sect_id=None, **kwargs):

	user = User.query.filter(or_(User.email==email, User.username==username)).first()

	if user:
		raise Exception('User already exists')

	user = User(email=email, name=name, username=username, password=password, country_id=country_id)

	user.encrypted_password = user.encrypt_password()

	db.session.add(user)
	try:
		db.session.commit()

		return user
	except:
		db.session.rollback()

def update_user(user_id, **kwargs):

	user = User.query.get(user_id)

	if not user:
		raise Exception('User not found')

	data = clean_dict(ignored_args, kwargs)

	user = populate_object(user, **data)

	db.session.add(user)

	try:
		db.session.commit()
		return user
	except:
		db.session.rollback()


def delete_user(user_id):

	user = User.query.get(user_id)

	if not user:
		raise Exception('User not found')

	db.session.delete(user)

	try:
		db.session.commit()
	except:
		db.session.rollback()