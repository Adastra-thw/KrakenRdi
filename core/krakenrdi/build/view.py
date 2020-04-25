from core.krakenrdi.server import Server
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import json
import os
import jsonschema

class BuildView():
	'''
	/build/list:
				Methods: GET, POST
				Request: {}
				Description: List every build created.

				Response:
				{
					builds: [
								{
									"buildName":"Build Name", 
									"buildDescription":"Build Description",
									"buildDate":"Build Date",
									"buildTools":"Number of tools",
									"buildContainers":"Build Containers",
								}, 
								{
									"buildName":"Build Name", 
									"buildDescription":"Build Description",
									"buildDate":"Build Date",
									"buildTools":"Number of tools",
									"buildContainers":"Build Containers",
								}
						]
					}
	'''
	@Server.app.route('/build/list', methods=["GET","POST"])
	def listTools():
		if request.is_json is False:
			abort(400)
		if not request.json or not 'stage' in request.json:
			abort(400)
		stage = request.json['stage']
		stages = {}
		tools = {}
		with open("config/tools.json", "r") as fdTools:
			stages = json.loads(fdTools.read())

		if stage in stages.keys():
			try:
				tools = stages[stage]
			except:
				abort(500)
		else:
			abort(404)
		return jsonify(tools)

	@Server.app.route('/recon/enable', methods=["GET","POST"])
	def enableTools(self):
	    return 'Hello, World!'