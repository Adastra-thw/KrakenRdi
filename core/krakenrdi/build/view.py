from core.krakenrdi.server.krakenServer import KrakenServer
from flask import Flask, jsonify
from flask import request, abort
from flask import make_response
import json, os, jsonschema
from core.krakenrdi.common.buildValidation import validateCreateBuild
from core.krakenrdi.build.tasks import createBuild, duplicateBuild

class BuildView():

	'''
	/build/list:
				Methods: GET, POST
				Request: {}
				Description: List every build created.
	'''
	@KrakenServer.restApi.route('/build/list', methods=["GET","POST"])
	def listBuilds():
		#tools = validateJson(request, abort)
		return jsonify(tools)

	'''
	/build/create:
			Response:
			{
				"message" : "Request for build creation received."			
			}
	'''
	@KrakenServer.restApi.route('/build/create', methods=["PUT","POST"])
	def createBuild():
		build = {}
		if validateCreateBuild(request, abort):
			#The JSON structure is valid, but before to save in database it's needed to send the task to Docker.
			celeryCreateBuildTask = createBuild.delay(request.json)
			print(celeryCreateBuildTask)
			#Create the build in database.
			print("create db")
			KrakenServer.database.builds.insert(request.json)
		return jsonify(build)

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
	@KrakenServer.restApi.route('/build/detail', methods=["POST"])
	def detailBuild():
		build = {}
		return jsonify(build)

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
	@KrakenServer.restApi.route('/build/delete', methods=["POST", "DELETE"])
	def deleteBuild():
		build = {}
		return jsonify(build)

	@KrakenServer.restApi.route('/build/filter', methods=["POST"])
	def filterBuild():
		build = {}
		return jsonify(build)

	@KrakenServer.restApi.route('/build/status', methods=["POST"])
	def statusBuild():
		build = {}
		return jsonify(build)
