from flask import Flask
from celery import Celery
import logging

class KrakenConfiguration():
	restApi = Flask(__name__)
	#
	# Initialize Celery
	taskEngine = Celery(restApi.name, 
						backend='redis://localhost:6379/0', 
						broker='redis://localhost:6379/0',
						include=['core.krakenrdi.backend.asyncro.tasks'])
	taskEngine.conf.update(restApi.config)
	database = None
	configuration = {}
	logging.basicConfig(filename='core/logs/krakenrdi.log', level=logging.DEBUG)