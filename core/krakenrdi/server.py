from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask_pymongo import PyMongo
import sys

class Server():
	app = Flask(__name__)
	krakenRdiDB = None
	
	@staticmethod
	def init(configuration, tools, arguments):
		#Database initialization
		Server.app.config['MONGO_DBNAME'] = configuration['config']['databaseName']
		Server.app.config['MONGO_URI'] = configuration['config']['databaseURI']
		try:
			#Connect with MongoServer.
			dbConnection = PyMongo(Server.app)
			krakenRdiDB = dbConnection.db
			krakenRdiDB.tools.insert(tools)
			krakenRdiDB.arguments.insert(arguments)
		except:
			print("Error in initialization of database. Check that your Mongo server is running at "+configuration['config']['databaseURI'])
			sys.exit(1)

	@staticmethod
	def getDatabase():
		return krakenRdiDB

	@staticmethod
	def startServer():
		Server.app.run()

	@app.errorhandler(500)
	def internal_error(error):
		return make_response(jsonify({'message': 'Internal server error processing the request.'}), 500)

	@app.errorhandler(400)
	def bad_request(error):
		return make_response(jsonify({'message': 'Invalid request. Read the docs.'}), 400)

	@app.errorhandler(404)
	def bad_request(error):
		return make_response(jsonify({'message': 'Resource not found'}), 404)