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
	/build/list:
				Methods: GET, POST
				Request: {}
				Description: List every build created.
	'''
	@KrakenConfiguration.restApi.route('/container/list', methods=["GET","POST"])
	def listContainers():
		response = KrakenServer.containerService.list()
		return jsonify(response)
	
	'''
	/build/create:
			Response:
			{
				"message" : "Request for build creation received."			
			}
	'''
	@KrakenConfiguration.restApi.route('/container/create', methods=["PUT","POST"])
	def createContainer():
		response = {}
		if validateApiRequest(request, abort, schema="createContainer"):
			structure = setDefaultsContainer(request.json)
			response = KrakenServer.containerService.create(request.json)
		return jsonify(response)