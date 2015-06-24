from flask.ext.sqlalchemy import SQLAlchemy
from locator import app, db, bcrypt
from datetime import datetime, date, time
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import dynamic
from sqlalchemy import func

class Base(object):

	@declared_attr
	def date_created(cls):
		return db.Column(db.DateTime, default=datetime.utcnow, index=True)

	@declared_attr
	def last_updated(cls):
		return db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

	def as_dict(self):

		data = inspect(self)

		return dict([(k, getattr(self, k)) for k in data.attrs.keys() if isinstance(getattr(self, k), (hybrid_property, db.Model, InstrumentedAttribute, InstrumentedList, dynamic.AppenderMixin)) is False])


class User(Base, db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False)
	gender = db.Column(db.String(64), nullable=True)
	username = db.Column(db.String(64), nullable=False)
	email = db.Column(db.String(200), nullable=False)
	password = db.Column(db.String(200), nullable=False)
	encrypted_password = db.Column(db.String(200), nullable=False)
	country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
	state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=True)
	sect_id = db.Column(db.Integer, db.ForeignKey('sect.id'), nullable=True)
	hadiths = db.relationship('Hadith', backref='hadith', lazy='dynamic')
	mosques = db.relationship('Mosque', backref='user', lazy='dynamic')
	banners = db.relationship('Banner', backref='banner', lazy='dynamic')
	duas = db.relationship('Dua', backref='dua', lazy='dynamic')


	def check_password(self, password):
		return bcrypt.check_password_hash(self.encrypted_password, password)

	def encrypt_password(self):
		return bcrypt.generate_password_hash(self.password)

class Mosque(Base, db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), nullable=False)
	line1 = db.Column(db.String(200), nullable=False)
	line2 = db.Column(db.String(200), nullable=True)
	country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
	state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	sect_id = db.Column(db.Integer, db.ForeignKey('sect.id'), nullable=True)
	prayer_type_id = db.Column(db.Integer, db.ForeignKey('prayer_type.id'), nullable=True)


class PrayerType(Base, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	code = db.Column(db.String(200), unique=True)
	mosques = db.relationship('Mosque', backref='prayer_type', lazy='dynamic')


class Sect(Base, db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	code = db.Column(db.String(200), unique=True)
	users = db.relationship('User', backref='sect', lazy='dynamic')
	mosques = db.relationship('Mosque', backref='sect', lazy='dynamic')

class Country(Base, db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	code = db.Column(db.String(200), unique=True)
	users = db.relationship('User', backref='country', lazy='dynamic')
	mosques = db.relationship('Mosque', backref='country', lazy='dynamic') 
	states = db.relationship('State', backref='country', lazy='dynamic')

class State(Base, db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	code = db.Column(db.String(200), unique=True)
	country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
	users = db.relationship('User', backref='state', lazy='dynamic')

class Hadith(Base, db.Model):

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	source = db.Column(db.String, nullable=False)
	text = db.Column(db.String, nullable=True)
	is_verified = db.Column(db.Boolean, default=False)

class Banner(Base, db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	url = db.Column(db.String, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Dua(Base, db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=True)
	source = db.Column(db.String, nullable=True)
	text = db.Column(db.String, nullable=False)
	is_live = db.Column(db.Boolean, default=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Event(Base, db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	mosque_id = db.Column(db.Integer, db.ForeignKey('mosque.id'), nullable=False)
	scheduled_date = db.Column(db.DateTime, nullable=False)
	image_url = db.Column(db.String)

# class Image(db.Model):

# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(200), nullable=False)

