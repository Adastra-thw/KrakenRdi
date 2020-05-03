from __future__ import absolute_import

import time
from celery import Celery, task
import json

from core.krakenrdi.server.CoreObjects import KrakenConfiguration
from core.krakenrdi.backend.connector.builder import DockerManagerConnection
'''
	Create a new build. If the docker build have success a new image will be generated. 
'''
@KrakenConfiguration.taskEngine.task(bind=True)
def createBuild(self, imageJson):

	buildStored = KrakenConfiguration.database.builds.find_one({"taskId": self.request.id})
	try:
		dockerManager = DockerManagerConnection()
		buildStored["taskState"] = {'status':'PROCESSING', 'message': 'Calling Docker service to create image.'}
		KrakenConfiguration.database.builds.update_one({'_id':buildStored["_id"]}, 
												{"$set": buildStored}, upsert=False)

		imageCreated= dockerManager.imageBuilder.build(imageJson)
		imageStore = json.loads(imageCreated)

		buildStored["taskState"] = {'status':'READY', 'message': 'Image created successfully and ready to create containers.'}
		KrakenConfiguration.database.builds.update_one({'_id':buildStored["_id"]}, 
												{"$set": buildStored}, upsert=False)

		imageStore["taskId"] = self.request.id
		KrakenConfiguration.database.builds_history.insert(imageStore)

		buildStored["taskState"] = {'status':'SAVED', 'message': 'Image logs saved successfully in database.'}
		KrakenConfiguration.database.builds.update_one({'_id':buildStored["_id"]}, 
												{"$set": buildStored}, upsert=False)
	except Exception as e:
		buildStored["taskState"] = {'status':'ERROR', 'message': 'There was an error running the image creation: '+str(e)}
		KrakenConfiguration.database.builds.update_one({'_id':buildStored["_id"]}, 
											{"$set": buildStored}, upsert=False)

	buildStored["taskState"] = {'status':'FINISHED', 'message': 'Task finished.'}
	KrakenConfiguration.database.builds.update_one({'_id':buildStored["_id"]}, 
											{"$set": buildStored}, upsert=False)
'''
	Duplicate an existing build
'''
@KrakenConfiguration.taskEngine.task()
def duplicateBuild(buildJson):
	print(222)