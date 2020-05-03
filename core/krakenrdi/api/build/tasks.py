from __future__ import absolute_import

import time
from celery import Celery, task
import json


'''
	Create a new build. If the docker build have success a new image will be generated. 
'''
@task()
def createBuild(imageJson):
	print("here")
	'''
	buildStored = KrakenManager.database.builds.find_one({"taskId": self.request.id})
	try:
		buildStored["taskState"] = {'status':'PROCESSING', 'message': 'Calling Docker service to create image.'}
		KrakenManager.database.builds.update_one({'_id':buildStored["_id"]}, 
												{"$set": buildStored}, upsert=False)

		imageCreated= manager.imageBuilder.build(imageJson)
		imageStore = json.loads(imageCreated)

		buildStored["taskState"] = {'status':'CREATED', 'message': 'Image created successfully and ready to create containers.'}
		KrakenManager.database.builds.update_one({'_id':buildStored["_id"]}, 
												{"$set": buildStored}, upsert=False)

		imageStore["taskId"] = self.request.id
		KrakenManager.database.builds_history.insert(imageStore)

		buildStored["taskState"] = {'status':'SAVED', 'message': 'Image logs saved successfully in database.'}
		KrakenManager.database.builds.update_one({'_id':buildStored["_id"]}, 
												{"$set": buildStored}, upsert=False)
	except Exception as e:
		buildStored["taskState"] = {'status':'ERROR', 'message': 'There was an error running the image creation: '+str(e)}
		KrakenManager.database.builds.update_one({'_id':buildStored["_id"]}, 
											{"$set": buildStored}, upsert=False)

	buildStored["taskState"] = {'status':'FINISHED', 'message': 'Task finished.'}
	KrakenManager.database.builds.update_one({'_id':buildStored["_id"]}, 
											{"$set": buildStored}, upsert=False)
	'''
'''
	Duplicate an existing build
'''
@task()
def duplicateBuild(buildJson):
	print(222)