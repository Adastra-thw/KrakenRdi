from core.krakenrdi.backend.async.tasks import createBuild
from core.krakenrdi.backend.connector.entities import Image, Container, Tool
import json
from jsonpickle import encode

class KrakenManager():

	database = None

	def __init__(self, database, configuration):
		self.database = database
		self.configuration = configuration
		self.buildService = None
		self.containerService = None
		self.toolService = None
	
	def getBuildService(self):
		if self.buildService is None:
			self.buildService = BuildService(self)
		return self.buildService

	def getContainerService(self):
		if self.containerService is None:
			self.containerService = ContainerService(self)
		return self.containerService

	def getToolService(self):
		if self.toolService is None:
			self.toolService = ToolService(self)
		return self.toolService


class BuildService():

	def __init__(self, manager):
		self.manager = manager

	def build(self, request):
		#The JSON structure is valid, but before to save in database it's needed to send the task to Docker.
		toolsEnabled = self.manager.database.tools.find({'name': {'$in': request['tools']} })
		toolsDisabled = self.manager.database.tools.find({'name': {'$nin': request['tools']} })

		imageCreate = Image()
		imageCreate.buildName = self.manager.configuration['config']['imageBase']+":"+request['buildName']
		imageCreate.buildScope=request['buildScope']
		imageCreate.startSSH=request['startSSH']
		imageCreate.startPostgres=request['startPostgres']

		'''
			Create the dict to dynamically create de images with parameters defined in Dockerfiles.
		'''
		for tool in toolsEnabled:
			if 'propertyEnabled' in tool:
				imageCreate.buildArgs[tool['propertyEnabled']] = 'True'
		for tool in toolsDisabled:
			if 'propertyEnabled' in tool:
				imageCreate.buildArgs[tool['propertyEnabled']] = 'False'

		if "containerProperties" in request:
			for containerProperty in request['containerProperties'].keys():
				if "EXPOSE_PORTS" in containerProperty:
					ports=""
					print(request['containerProperties']["EXPOSE_PORTS"])
					ports = ' '.join(map(str, request['containerProperties']["EXPOSE_PORTS"]))
					print(ports)
					imageCreate.buildArgs[containerProperty] = ports
				else:
					imageCreate.buildArgs[containerProperty] = request['containerProperties'][containerProperty]
				
		'''self.buildScope=None
		self.memoryLimit=None
		self.extraHostIP=None #--add-host=docker:10.180.0.1				
		'''
		import secrets 
		taskId=imageCreate.buildName+"-"+str(secrets.token_hex(8))
		result = json.loads(encode(imageCreate).replace("\\",""))
		result.pop("py/object", None)
		result["tools"] = request['tools']
		result["taskId"] = taskId
		result["taskState"] = "CREATED"

		#Create the build in database.
		self.manager.database.builds.insert(result)
		#Run celery task with apply_async
		celeryCreateBuildTask = createBuild.apply_async((encode(imageCreate),), 
														task_id=taskId)
		del(result["_id"])
		return result
		

	def list(self):
		buildsStored = self.manager.database.builds.find({})
		response = []
		for build in buildsStored:
			response.append({'buildName': build['buildName'], 
						 'buildScope': build['buildScope'], 
						 'tools': build['tools'],
						 'containerProperties': build['buildArgs'], 
						 'startSSH': build['startSSH'],
						 'startPostgres': build['startPostgres'], 
						 'taskState': build['taskState'], 
						 'memoryLimit': build['memoryLimit']})
		return response

	def filter(self):
		pass

class ContainerService():
	def __init__(self, manager):
		self.manager = manager

	def create(self):
		pass
	def execute(self):
		pass
	def destroy(self):
		pass

class ToolService():
	def __init__(self, manager):
		self.manager = manager

	pass