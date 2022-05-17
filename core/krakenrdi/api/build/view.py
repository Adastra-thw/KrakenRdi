from core.krakenrdi.server.CoreObjects import KrakenConfiguration
from core.krakenrdi.server.krakenServer import KrakenServer

from flask import jsonify
from flask import request, abort
from flask import make_response
import json, os, jsonschema
from core.krakenrdi.api.common.validations import validateApiRequest, setDefaultsBuild
from jsonpickle import encode
from flask import jsonify

class BuildView():


	'''
	/build/list:
				Methods: GET, POST
				Request: {}
				Description: List every build created.
	'''
	@KrakenConfiguration.restApi.route('/build/list', methods=["GET","POST"])
	def listBuilds():
		response = KrakenServer.buildService.list()
		return jsonify(response)
	
	'''
	/build/create:
			Response:
			{
				"message" : "Request for build creation received."			
			}
	'''
	@KrakenConfiguration.restApi.route('/build/create', methods=["PUT","POST"])
	def createBuild():
		response = {}
		if KrakenConfiguration.taskEngine.control.inspect().active() is None:
			#Celery worker is Down. It should avoid to continue and warn the client.
			response = {"message": "Celery worker is down. Start the KrakenRDI worker using '-w' option"}
		else:
			if validateApiRequest(request, abort, schema="createBuild"):
				structure = setDefaultsBuild(request.json)
				response = KrakenServer.buildService.build(structure)
		return jsonify(response)

	'''
			{	
				"buildStages": ["common","framework","candc","delivery",
	  							"escalation","exfiltration","exploitation",
	  							"internalrecon","movelateral","recon","weapon","all"],
	  			"buildTools" : [{
									"toolName": "Tool's name",
									"toolDescription": "Tool's description",
									"toolURL": "Tool's URL",
									"toolScope" ["PT","RT"]
								}, 
								{	
									"toolName": "Tool's name2",
									"toolDescription": "Tool's description2",
									"toolURL": "Tool's URL2",
									"toolScope" ["PT","RT"]
								}]
			}, 
	'''
	@KrakenConfiguration.restApi.route('/build/detail', methods=["POST"])
	def detailBuild():
		response = {}
		if validateApiRequest(request, abort, schema="detailBuild"):
			structure = setDefaultsBuild(request.json)
			response = KrakenServer.buildService.detail(structure)
		return jsonify(response)

	'''
			{	
				"buildStages": ["common","framework","candc","delivery",
	  							"escalation","exfiltration","exploitation",
	  							"internalrecon","movelateral","recon","weapon","all"],
	  			"buildTools" : [{
									"toolName": "Tool's name",
									"toolDescription": "Tool's description",
									"toolURL": "Tool's URL",
									"toolScope" ["PT","RT"]
								}, 
								{	
									"toolName": "Tool's name2",
									"toolDescription": "Tool's description2",
									"toolURL": "Tool's URL2",
									"toolScope" ["PT","RT"]
								}]
			}, 
	'''

	'''
	Destroy the related build. Restrictions:
		1. If the task is PENDING, it can't be removed.
		2. If the parameter "force" is set to "True" it should remove the build from database no matter if is PENDING.
		3. Before remove.
			1- It should check the restrictions above.
			2- Call a Celery task to check if the image still exists in docker. 
				If it exists, try to remove it. If not, continue to the next step.
			3- Remove the image from the Docker daemon.
		4. If the image could be removed from the Docker daemon, let remove it from database.
			it should remove the image from the collection "builds"
	'''
	@KrakenConfiguration.restApi.route('/build/delete', methods=["POST", "DELETE"])
	def deleteBuild():
		response = {}
		if validateApiRequest(request, abort, schema="deleteBuild"):
			structure = setDefaultsBuild(request.json)
			response = KrakenServer.buildService.delete(structure)
		return jsonify(response)

	@KrakenConfiguration.restApi.route('/build/filter', methods=["POST"])
	def filterBuild():
		build = {}
		return jsonify(build)

	'''
		This should check 2 things.
			1. The state in database
			2. The state in docker daemon.
		The reponse to the client includes the state in database and the state in Docker daemon.
		if the image don't exists in Docker enginee but is PENDING in database, probable the task
		has failed.
	'''
	@KrakenConfiguration.restApi.route('/build/status', methods=["POST"])
	def statusBuild():
		build = {}
		return jsonify(build)
