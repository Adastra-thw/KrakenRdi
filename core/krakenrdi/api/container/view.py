from core.krakenrdi.server.CoreObjects import KrakenConfiguration
from core.krakenrdi.server.krakenServer import KrakenServer

from flask import jsonify
from flask import request, abort
from flask import make_response
import json, os, jsonschema
from core.krakenrdi.api.common.validations import validateApiRequest, setDefaultsContainer
from jsonpickle import encode
from flask import jsonify

class ContainerView():

	'''
	/container/list:
				Methods: GET, POST
				Request: {}
				Description: List every build created.
	'''
	@KrakenConfiguration.restApi.route('/container/list', methods=["GET","POST"])
	def listContainers():
		response = KrakenServer.containerService.list()
		return jsonify(response)

	'''
	/container/get:
				Methods: POST
				Request: {"containerName": "<NAME_OF_CONTAINER>"}
				Description: List every build created.
	'''
	@KrakenConfiguration.restApi.route('/container/get', methods=["POST"])
	def getContainer():
		response = {}
		if validateApiRequest(request, abort, schema="getContainer"):
			structure = setDefaultsContainer(request.json)
			response = KrakenServer.containerService.get(structure)
		return jsonify(response)
	

	'''
	/build/create:
				Methods: PUT, POST
				Request:
					{ 	"buildName": "<buildName>",
    					"containerName": "<containerName>",
    					"autoRemove": true|false,
    					"capAdd": ["CAP1", "CAP2", "CAPN"],
    					"capDrop": ["CAP1", "CAP2", "CAPN"], 
					    "hostname":  "<hostname>",
    					"memoryLimit": "<memoryLimit>",
						"networkMode": "<networkMode>",
    					"networkDisabled": true|false,
						"readOnly": true|false,
						"removeOnFinish": true|false,
    					"removeIfExists": true|false,
    					"ports": [ {"protocolHost": "tcp|udp",
                						"portHost": <portHost>,
                						"protocolContainer": "tcp|udp",
                						"portContainer": <portContainer>
                					}],
    					"volumes": [{"hostVolume" : "<hostVolume>", 
                    				 	"containerVolume" : "containerVolume",
                    					"modeVolume" : "rw|ro" }]
					}

				Description: Creates a new container in Docker service and save it in database.
	'''
	@KrakenConfiguration.restApi.route('/container/create', methods=["PUT","POST"])
	def createContainer():
		response = {}
		if validateApiRequest(request, abort, schema="createContainer"):
			structure = setDefaultsContainer(request.json)
			response = KrakenServer.containerService.create(structure)
		return jsonify(response)

	'''
	/container/delete:
				Methods: PUT, POST
				Request: {"containerName": "<NAME_OF_CONTAINER>"}
				Description: Deletes the specified container by name.
	'''
	@KrakenConfiguration.restApi.route('/container/delete', methods=["PUT","POST"])
	def deleteContainer():
		response = {}
		if validateApiRequest(request, abort, schema="deleteContainer"):
			structure = setDefaultsContainer(request.json)
			response = KrakenServer.containerService.delete(structure)
		return jsonify(response)

	'''
	/container/stop:
				Methods: PUT, POST
				Request: {"containerName": "<NAME_OF_CONTAINER>"}
				Description: Stops the specified container by name.
	'''
	@KrakenConfiguration.restApi.route('/container/stop', methods=["PUT","POST"])
	def stopContainer():
		response = {}
		if validateApiRequest(request, abort, schema="stopContainer"):
			structure = setDefaultsContainer(request.json)
			response = KrakenServer.containerService.stop(structure)
		return jsonify(response)		