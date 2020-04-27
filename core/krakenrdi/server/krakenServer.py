from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask_pymongo import PyMongo
from celery import Celery, task
import sys

class KrakenServer():
	restApi = Flask(__name__)
	#
	# Initialize Celery
	taskEngine = Celery(restApi.name, 
						backend='redis://localhost:6379/0', 
						broker='redis://localhost:6379/0',
						include=['core.krakenrdi.build'])
	taskEngine.conf.update(restApi.config)
	database = None
	
	@staticmethod
	def init(configuration, tools, arguments):
		KrakenServer.restApi.config['DEBUG'] = True
		#Database initialization
		KrakenServer.restApi.config['MONGO_DBNAME'] = configuration['config']['databaseName']
		KrakenServer.restApi.config['MONGO_URI'] = configuration['config']['databaseURI']
		# Celery configuration
		KrakenServer.restApi.config['CELERY_BROKER_URL'] = configuration['config']['celeryBrokerUrl']
		KrakenServer.restApi.config['CELERY_RESULT_BACKEND'] = configuration['config']['celeryResultBackend']

		try:
			#Connect with MongoKrakenServer.
			dbConnection = PyMongo(KrakenServer.restApi)
			KrakenServer.database = dbConnection.db
			if "arguments" not in KrakenServer.database.list_collection_names():
				KrakenServer.database.arguments.insert(arguments)
			if "tools" not in KrakenServer.database.list_collection_names():
				KrakenServer.database.tools.insert(tools)
		except:
			print("Error in initialization of database. Check that your Mongo server is running at "+configuration['config']['databaseURI'])
			sys.exit(1)

	@restApi.errorhandler(500)
	def internal_error(error):
		return make_response(jsonify({'message': str(error)}), 500)

	@restApi.errorhandler(400)
	def bad_request(error):
		return make_response(jsonify({'message': str(error)}), 400)

	@restApi.errorhandler(404)
	def bad_request(error):
		return make_response(jsonify({'message': 'Resource not found'}), 404)