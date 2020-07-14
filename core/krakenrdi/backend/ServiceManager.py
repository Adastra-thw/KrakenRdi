from core.krakenrdi.backend.async.tasks import createBuild
from core.krakenrdi.backend.connector.entities import Image, Container, Tool
from core.krakenrdi.backend.connector.builder import DockerManagerConnection
from core.krakenrdi.api.common.validations import BusinessValidations
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
		self.dockerManager = DockerManagerConnection()
		self.businessValidations = BusinessValidations(self.dockerManager)

	
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

	def __getBuilds(self, buildsStored):
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


	def build(self, request):
		#Before to begin, check the name of the image. If it already exists shoud avoid to continue, 
		# except if the parameter "overwrite" is "True"
		result={}
		build = self.manager.database.builds.find({'buildName': self.manager.configuration['config']['imageBase']+":"+request['buildName']} )
		if len(list(build)) > 0 and request["overwrite"] is False:
			return {"message": "The name of the image already used. Choose another one or if you want to overwrite that image, send 'overwrite' parameter in the JSON structure."}

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
					ports = ' '.join(map(str, request['containerProperties']["EXPOSE_PORTS"]))
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
		createBuild.apply_async((encode(imageCreate),), task_id=taskId)
		del(result["_id"])
		return result
		

	def list(self):
		buildsStored = self.manager.database.builds.find({})
		return self.__getBuilds(buildsStored)

	def detail(self, request):
		buildsStored = self.manager.database.builds.find({'buildName': self.manager.configuration['config']['imageBase']+":"+request['buildName']} )
		return self.__getBuilds(buildsStored)

	def filter(self):
		pass

class ContainerService():
	def __init__(self, manager):
		self.manager = manager

	def create(self, request):
		#Before to begin, check the name of the image. If it doesn't exists shoud avoid to continue.
		result={}
		if "buildName" in request:
			build = self.manager.database.builds.find({'buildName': self.manager.configuration['config']['imageBase']+":"+request['buildName']} )
			if len(list(build)) == 0:
				result = {"message": "The specified image "+request['buildName']+" doesn't exists" }
			else:
				stateBuild = self.manager.database.builds.find({'taskState.status': {'$in': ["READY", "SAVED", "FINISHED"] } } )
				if len(list(stateBuild)) > 0:
					request['buildName']=self.manager.configuration['config']['imageBase']+":"+request['buildName']
					containerStructure = self.manager.businessValidations.validateContainerStructure(request)
					container = Container()					
					container.buildName=containerStructure["buildName"]
					container.containerName=containerStructure["containerName"]
					container.capAdd=containerStructure["capAdd"]
					container.capDrop=containerStructure["capDrop"]
					container.hostname=containerStructure["hostname"]
					container.memoryLimit=containerStructure["memoryLimit"]
					container.networkMode=containerStructure["networkMode"]
					container.networkDisabled=containerStructure["networkDisabled"]
					container.readOnly=containerStructure["readOnly"]
					container.ports=containerStructure["ports"]
					container.volumes=containerStructure["volumes"]
					#Create the container in Docker.
					self.manager.dockerManager.containerBuilder.create(container)
					#Register the container in database if it was sucessfully created in Docker.
				else:
					result = {"message": "The image "+request['buildName']+" is not ready yet. The image is still in creation process."}
		else:
			result = {"message": "You have to specify the field 'buildName' with the name of the image that will be used to create the container."}
		return result

	def execute(self):
		pass
	def destroy(self):
		pass

class ToolService():
	def __init__(self, manager):
		self.manager = manager

	def __getTools(self, toolsStored):
		response = []
		for tool in toolsStored:
			response.append({'toolName': tool['name'], 
						'toolDescription': tool['description'],
						'toolURL': tool['url'],
						'toolScope': {"RT": tool['RT'], "PT": tool['PT']} 
						})
		return response


	def list(self):
		toolsStored = self.manager.database.tools.find({})
		return self.__getTools(toolsStored)

	def filter(self, request):
		toolsStored = self.manager.database.tools.find( {'name': {'$regex': request['toolName'], "$options": "-i"} })
		return self.__getTools(toolsStored)

	def info(self):
		pass
