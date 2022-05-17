from __future__ import absolute_import, unicode_literals
import json
import os,sys
import jsonschema
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask_pymongo import PyMongo
from celery import Celery, task
from celery import current_app
from celery.bin import worker
import sys
from core.krakenrdi.build.tasks import createBuild

start= True
celery = Celery('testing_celery',	backend='redis://localhost:6379/0', 
							broker='redis://localhost:6379/0')
celery.autodiscover_tasks(['core.krakenrdi.build'])
if start:
	app = Flask(__name__)
	app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
	app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
	#krakenTaskEngine = Celery(app.name, backend='redis://localhost:6379/0', broker='redis://localhost:6379/0', include=['core.krakenrdi.build.tasks'])
	application = current_app._get_current_object()
	worker = worker.worker(app=application)
	options = {
		'broker': app.config['CELERY_BROKER_URL'],
		'loglevel': 'INFO',
		'traceback': True,
	}
	worker.run(**options)