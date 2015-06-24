from locator import app, logger, db
from locator.core.utilities import code_generator, populate_object, clean_dict
import requests
import json, urllib
from locator.models import *
from sqlalchemy import and_, or_

ignored_args = ['id', 'last_updated', 'date_created']


def load_mosques(latitude, longitude, **kwargs):

	api_key = app.config.get('API_KEY')

	url = app.config.get('PLACE_URL') + '/nearbysearch/json'

	data = {
		'location': '%s,%s' %(latitude, longitude),
		'radius': 500,
		'types': 'mosque',
		'key': api_key
	}

	resp = requests.get(url, data)

	response = json.loads(resp.content).get('results')

	return response

def place_details_search(place_id):

	api_key = app.config.get('API_KEY')

	url = app.config.get('PLACE_URL') + '/details/json'

	data = {
		'place_id': place_id,
		'key': api_key
	}

	resp = requests.get(url, data)

	response = json.loads(resp.content).get('results')

	return response

def create_hadith(user_id, source, text, **kwargs):

	user = User.query.get(user_id)

	if not user:
		raise Exception('User not found')

	hadith = Hadith(user_id=user.id, text=text, source=source)

	db.session.add(hadith)

	try:
		db.session.commit()

		return hadith
	except:
		db.session.rollback()

def update_hadith(hadith_id, **kwargs):

	hadith = Hadith.query.get(hadith_id)

	if not hadith:
		raise Exception('Hadith not found')

	data = clean_dict(ignored_args, kwargs)

	hadith = populate_object(hadith, **data)

	db.session.add(hadith)

	try:
		db.session.commit()
		return hadith
	except:
		db.session.rollback()

def delete_hadith(hadith_id, **kwargs):

	hadith = Hadith.query.get(hadith_id)

	if not hadith:
		raise Exception('Hadith not found')

	db.session.delete(hadith)

	try:
		db.session.commit()
	except:
		db.session.rollback()

def verify_hadith(hadith_id):

	hadith = Hadith.query.get(hadith_id)

	if not hadith:
		raise Exception('Hadith not found')

	hadith.is_verified = True

	db.session.add(hadith)

	try:
		db.session.commit()
		return hadith
	except:
		db.session.rollback()

def invalidate_hadith(hadith_id):

	hadith = Hadith.query.get(hadith_id)

	if not hadith:
		raise Exception('Hadith not found')

	hadith.is_verified = False

	db.session.add(hadith)

	try:
		db.session.commit()
		return hadith
	except:
		db.session.rollback()

def create_dua(text, user_id, name=None, source=None, **kwargs):

	user = User.query.get(user_id)

	if not user:
		raise Exception('User not found')

	dua = Dua.query.filter(or_(Dua.name==name, Dua.text==text)).first()

	logger.info(dua)

	if dua:
		return dua

	dua = Dua(name=name, text=text, source=source, user_id=user.id)

	logger.info(dua)

	db.session.add(dua)

	try:
		db.session.commit()
		return dua
	except:
		db.session.rollback()

def update_dua(dua_id, **kwargs):

	dua = Dua.query.get(dua_id)

	if not dua:
		raise Exception('Dua not found')

	data = clean_dict(ignored_args, kwargs)

	dua = populate_object(dua, **data)

	db.session.add(dua)

	try:
		db.session.commit()
		return dua
	except:
		db.session.rollback()

def delete_dua(dua_id):

	dua = Dua.query.get(dua_id)

	if not dua:
		raise Exception('Dua not found')

	db.session.delete(dua)

	try:
		db.session.commit()

	except:
		db.session.rollback()



