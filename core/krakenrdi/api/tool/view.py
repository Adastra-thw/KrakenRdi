from core.krakenrdi.server.CoreObjects import KrakenConfiguration
from core.krakenrdi.server.krakenServer import KrakenServer

from flask import jsonify
from flask import request, abort
from flask import make_response
import json, os, jsonschema
from core.krakenrdi.api.common.validations import validateApiRequest, setDefaultsTool
from jsonpickle import encode
from flask import jsonify

class ToolView():
	
	'''
	/tools/stages:
				Methods: GET, POST
				Request: {}
				Description: List of stages for tools.

				Response:
				{"toolStages" : ["common","framework","candc","delivery",
						  				"escalation","exfiltration","exploitation",
						  				"internalrecon","movelateral","recon","weapon","all"]
				} 

	'''
	def stagesTools(self, requestJson):
		pass

	@KrakenConfiguration.restApi.route('/tools/list', methods=["GET","POST"])
	def listTools():
		response = KrakenServer.toolService.list()
		return jsonify(response)


	'''
	/tools/info:
				Methods: POST
				Request: {"toolName" : "Tool's name"}
				Description: Get basic information about one tool
				Response:
				{
					"toolName": "Tool's name",
					"toolDescription": "Tool's description",
					"toolURL": "Tool's URL",
					"toolScope" ["PT","RT"]
				}
	'''
	@KrakenConfiguration.restApi.route('/tools/info', methods=["POST"])
	def infoTools():
		response = {}
		if validateApiRequest(request, abort, schema="infoToolSchema"):
			structure = setDefaultsTool(request.json)
			response = KrakenServer.toolService.info(structure)
		return jsonify(response)

	'''
	/tools/filter:
				Methods: POST
				Request: {"toolName" : "hydra",
						  "toolStage" : ["common","framework","candc","delivery",
						  				"escalation","exfiltration","exploitation",
						  				"internalrecon","movelateral","recon","weapon","all"]
						  }
				Description: List of tools by scope and stage.

				Response:
				{	
					"tools" {
								[
									{
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
									}
								]
					}
				}
	'''
	@KrakenConfiguration.restApi.route('/tools/filter', methods=["POST"])
	def filterTools():
		response = {}
		if validateApiRequest(request, abort, schema="filterToolSchema"):
			structure = setDefaultsTool(request.json)
			response = KrakenServer.toolService.filter(structure)
		return jsonify(response)