from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from config import *
import os
from factories import create_app

app = create_app('masjid', Config)

manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def syncdb(refresh):

	"""
	logic to create and drop database
	"""

	from locator.models import *
	if refresh:
		db.drop_all()
	db.create_all()
	db.session.flush()

@manager.command
def setup_files():

	from startup import *

	upload_countries()

	upload_states(name='Nigeria')

@manager.command
def runserver():

	"""
	running application
	"""

	from factories import initialize_api
	from locator.resources.base import *

	initialize_api(app, app.api)

	with app.app_context():

		port = int(os.environ.get('PORT', 5000))
		app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
	manager.run()