from core.krakenrdi.server.CoreObjects import KrakenConfiguration
from core.krakenrdi.server.krakenServer import KrakenServer

from flask import jsonify
from flask import request, abort
from flask import make_response
import json, os, jsonschema
from core.krakenrdi.api.common.validations import validateCreateBuild
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
		if validateCreateBuild(request, abort):
			response = KrakenServer.buildService.build(request.json)
		return response

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
	@KrakenConfiguration.restApi.route('/build/delete', methods=["POST", "DELETE"])
	def deleteBuild():
		build = {}
		return jsonify(build)

	@KrakenConfiguration.restApi.route('/build/filter', methods=["POST"])
	def filterBuild():
		build = {}
		return jsonify(build)

	@KrakenConfiguration.restApi.route('/build/status', methods=["POST"])
	def statusBuild():
		build = {}
		return jsonify(build)
