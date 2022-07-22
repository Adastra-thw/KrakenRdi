from core.krakenrdi.backend.asyncro.tasks import createBuild
from core.krakenrdi.backend.connector.entities import Image, Container, Tool
from core.krakenrdi.backend.connector.builder import DockerManagerConnection
from core.krakenrdi.api.common.validations import BusinessValidations
import json
from jsonpickle import encode
from docker.errors import ImageNotFound

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
			shortName = build['buildName']
			if len(build['buildName'].split(':')) > 0:
				shortName = build['buildName'].split(':')[1]
			
			response.append({'buildFullName': build['buildName'], 
						 'buildName': shortName,
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
		buildName= self.manager.configuration['config']['imageBase']+":"+request['buildName']
		buildFound = self.manager.database.builds.find({'buildName': buildName} )
		numberBuilds = len(list(buildFound))
		if numberBuilds > 0 and request["overwrite"] is False:
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
		if numberBuilds > 0 and request["overwrite"] == True:
			#The build exist in database and "overwrite" is True, it should be deleted from Database.
			self.manager.database.builds.delete_one({'buildName': buildName})
		self.manager.database.builds.insert_many([result])
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

	def delete(self, request):
		#Before to remove from database, remove from Docker daemon.
		result = {}
		try:
			result = self.manager.dockerManager.imageBuilder.delete(self.manager.configuration['config']['imageBase']+":"+request['buildName'])
		except ImageNotFound:
			return {"message": "Image not found in Docker service. If it existed in database it was already deleted too"}
		finally:
			self.manager.database.builds.delete_one({'buildName': self.manager.configuration['config']['imageBase']+":"+request['buildName']} )
			return result


	def filter(self):
		pass

class ContainerService():
	def __init__(self, manager):
		self.manager = manager
	
	def list(self):
		result={}
		containers = self.manager.database.containers.find()
		for container in containers:
			result["buildName"] = container["buildName"] 
			result["containerName"] = container["containerName"]
			result["containerPorts"] = container["ports"]
			result["containerVolumes"] = container["volumes"]
			#Get the status for this container in Docker Daemon.
			result["containerStatus"] = self.manager.dockerManager.containerBuilder.checkStatus(container["containerName"])
		return result

	def get(self, request):
		containerFound = self.manager.database.containers.find_one({"containerName": request["containerName"]})
		if containerFound is not None:
			del(containerFound["_id"])
			return containerFound
		else:
			return {"message": "Container not found in database."}




	def create(self, request):
		#Before to begin, check the name of the image. If it doesn't exists shoud avoid to continue.
		result={}
		if "buildName" in request:
			build = self.manager.database.builds.find({'buildName': self.manager.configuration['config']['imageBase']+":"+request['buildName']} )
			if len(list(build)) == 0:
				result = {"message": "The specified image "+request['buildName']+" doesn't exists" }
			else:
				stateBuild = self.manager.database.builds.find_one({'taskState.status': {'$in': ["READY", "SAVED", "FINISHED"] } } )
				if stateBuild is not None:
					request['buildName']=self.manager.configuration['config']['imageBase']+":"+request['buildName']
					containerStructure = self.manager.businessValidations.validateContainerStructure(request)
					if containerStructure["valid"] is False:
						return containerStructure
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
					container.environment=containerStructure["environment"]
					#Create the container in Docker.
					dockerContainer = self.manager.dockerManager.containerBuilder.create(container)
					#The container instance will be useful to start sevices depending on the Image spec.

					if stateBuild["startSSH"]:
						dockerContainer.exec_run("/etc/init.d/ssh start", user="root")
						from os import environ
						dockerContainer.exec_run("export DISPLAY="+environ["DISPLAY"])
						container.startSSH = True
					if stateBuild["startPostgres"]:
						dockerContainer.exec_run("/etc/init.d/postgresql start", user="root")				
						container.startSSH = True
					
					#Register the container in database if it was sucessfully created in Docker.
					result = {
							"containerId": dockerContainer.id, 
							"containerImage": dockerContainer.attrs, 
							"containerName": dockerContainer.name, 
							"containerStatus": dockerContainer.status}
					
					self.manager.database.containers.delete_one({'containerName': dockerContainer.name } )
					containerJson = json.loads(encode(container).replace("\\","").replace(".",""))
					containerJson.pop("py/object", None)
					self.manager.database.containers.insert_many(containerJson)

				else:
					result = {"message": "The image "+request['buildName']+" is not ready yet. The image is still in creation process."}
		else:
			result = {"message": "You have to specify the field 'buildName' with the name of the image that will be used to create the container."}
		return result

	def delete(self, request):
		result={}
		rmDatabase=True
		#Delete container from Database and later from docker engine.
		try:	
			self.manager.database.containers.delete_one({"containerName": request["containerName"]})
		except:
			rmDatabase = False
		finally:
			success = self.manager.dockerManager.containerBuilder.delete(request["containerName"])
			if success and rmDatabase:
				result["message"] = "Container removed from database and Docker engine."
			elif success and rmDatabase is False:
				result["message"] = "Container removed from Docker engine but it can't be removed from Database. Seems the document in database don't exists."
			elif success is False and rmDatabase:
				result["message"] = "Container removed from database but it can't be removed from Docker engine. Seems the docker is being used by other process or don't exists."
			elif success is False and rmDatabase is False:
				result["message"] = "Container can't be removed from Docker engine and database. Maybe the container's name specified is wrong."
		return result

	def stop(self, request):
		result={}
		try:	
			self.manager.database.containers.update_one({"containerName": request["containerName"]})
		except:
			rmDatabase = False
		finally:
			success = self.manager.dockerManager.containerBuilder.delete(request["containerName"])
			if success and rmDatabase:
				result["message"] = "Container removed from database and Docker engine."
			elif success and rmDatabase is False:
				result["message"] = "Container removed from Docker engine but it can't be removed from Database. Seems the document in database don't exists."
			elif success is False and rmDatabase:
				result["message"] = "Container removed from database but it can't be removed from Docker engine. Seems the docker is being used by other process or don't exists."
			elif success is False and rmDatabase is False:
				result["message"] = "Container can't be removed from Docker engine and database. Maybe the container's name specified is wrong."
		return result


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
