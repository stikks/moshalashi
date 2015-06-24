from locator import app, db, logger
import os, json
from locator.models import *

DEFAULT_DIR = app.config.get('DEFAULT_DIR')

def upload_countries():

	filepath = os.path.join(DEFAULT_DIR, 'countries.json')

	logger.info(filepath)

	_file = open(filepath)

	data = json.loads(_file.read().encode("UTF-8"))

	for item in data:

		country = Country(name=item.get('name'), code=item.get('code'))
		db.session.add(country)
		try:
			db.session.commit()
			logger.info(country)
		except:
			db.session.rollback()


def upload_states(name):

	country = Country.query.filter(func.lower(Country.name)==name.lower()).first()

	filepath = os.path.join(DEFAULT_DIR, 'states/%s.json'%country.name.lower())

	logger.info(filepath)

	_file = open(filepath)

	data = json.loads(_file.read().encode("UTF-8"))

	for key, value in data.items():

		state = State(name=value, code=key, country_id=country.id)

		db.session.add(state)
		try:
			db.session.commit()
		except:
			db.session.rollback()


