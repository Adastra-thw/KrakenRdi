from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
import json
import os
import jsonschema

app = Flask(__name__)

'''
Available endpoints:
/config/docker				Configuration for Docker daemon

/recon/list					List of tools available.
/recon/enable				Selection of enabled tools.
/recon/generate				Generate image.
/recon/settings				Set configuration options: General and tools specific.
/recon/container/create
/recon/container/status
/recon/container/stop
/recon/container/remove
/recon/container/prune
'''

'''
Stages:	"recon", "weaponization", "delivery", "exploitation", 
		"persistence", "commandcontrol", "interalrecon", "movelaterally", "exfiltrate"

{"stage":"recon"}

'''
@app.route('/recon/list', methods=["GET","POST"])
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

@app.route('/recon/enable', methods=["GET","POST"])
def enableTools():
    return 'Hello, World!'

@app.route('/recon/settings', methods=["GET","POST"])
def settings():
    return 'Hello, World!'

@app.route('/recon/generate', methods=["GET","POST"])
def generateImage():
    return 'Hello, World!'




@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({'message': 'Internal server error processing the request.'}), 500)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'message': 'Invalid request. Read the docs.'}), 400)

@app.errorhandler(404)
def bad_request(error):
    return make_response(jsonify({'message': 'Resource not found'}), 404)


if __name__ == '__main__':
    app.run()