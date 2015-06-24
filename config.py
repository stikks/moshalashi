import os


class Config(object):
	DEBUG = True
	SECRET_KEY = '\x91c~\xc0-\xe3\'f\xe19PE\x93\xe8\x91`uu"\xd0\xb6\x01/\x0c\xed\\\xbd]H\x99k\xf8'
	SQLALCHEMY_ECHO = False
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/masjid'
	DEFAULT_DIR = os.path.abspath('startup')

	#google API KEY
	API_KEY = 'AIzaSyC6iPANJCIRU9fUNXMKr5gt3pyKGgOqjiE'
	PLACE_URL = 'https://maps.googleapis.com/maps/api/place'

# DATABASE = SQLALCHEMY_DATABASE_URI