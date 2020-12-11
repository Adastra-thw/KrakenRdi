from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask_pymongo import PyMongo
from celery import Celery, task
import sys
from core.krakenrdi.server.CoreObjects import KrakenConfiguration
from core.krakenrdi.backend.ServiceManager import KrakenManager

class KrakenServer():
	
	buildService = None
	containerService = None
	toolService = None
	'''
	Create singletons for managers of the application.
	'''
	@staticmethod
	def configureServices():
		coreManager = KrakenManager(database=KrakenConfiguration.database, 
									configuration=KrakenConfiguration.configuration)
		KrakenServer.buildService=coreManager.getBuildService()
		KrakenServer.containerService=coreManager.getContainerService()
		KrakenServer.toolService=coreManager.getToolService()


	@staticmethod
	def init(configuration, tools, arguments, cleanDB):
		KrakenConfiguration.configuration = configuration
		KrakenConfiguration.restApi.config['DEBUG'] = True
		#Database initialization
		KrakenConfiguration.restApi.config['MONGO_DBNAME'] = configuration['config']['databaseName']
		KrakenConfiguration.restApi.config['MONGO_URI'] = configuration['config']['databaseURI']
		# Celery configuration
		KrakenConfiguration.restApi.config['CELERY_BROKER_URL'] = configuration['config']['celeryBrokerUrl']
		KrakenConfiguration.restApi.config['CELERY_RESULT_BACKEND'] = configuration['config']['celeryResultBackend']
		KrakenConfiguration.restApi.config['CELERY_TRACK_STARTED'] = True
		KrakenConfiguration.restApi.config['CELERY_SEND_EVENTS'] = True
		KrakenConfiguration.taskEngine.conf.update(KrakenConfiguration.restApi.config)
		
		try:
			#Connect with MongoKrakenServer.
			dbConnection = PyMongo(KrakenConfiguration.restApi)
			KrakenConfiguration.database = dbConnection.db
			if cleanDB:
				for collectionDB in KrakenConfiguration.database.list_collection_names():
					KrakenConfiguration.database.drop_collection(collectionDB)
			if "arguments" not in KrakenConfiguration.database.list_collection_names():
				KrakenConfiguration.database.arguments.insert(arguments)
			if "tools" not in KrakenConfiguration.database.list_collection_names():
				KrakenConfiguration.database.tools.insert(tools)
		except:
			print("Error in initialization of database. Check that your Mongo server is running at "+configuration['config']['databaseURI'])
			sys.exit(1)
		#KrakenServer.manager = KrakenManager(database=KrakenServer.database, 
        #									 configuration=KrakenServer.configuration)

	@KrakenConfiguration.restApi.errorhandler(500)
	def internal_error(error):
		return make_response(jsonify({'message': str(error)}), 500)

	@KrakenConfiguration.restApi.errorhandler(400)
	def bad_request(error):
		return make_response(jsonify({'message': str(error)}), 400)

	@KrakenConfiguration.restApi.errorhandler(404)
	def not_found_request(error):
		return make_response(jsonify({'message': 'Resource not found'}), 404)