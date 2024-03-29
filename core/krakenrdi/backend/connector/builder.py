from core.krakenrdi.server.CoreObjects import KrakenConfiguration
import docker 
from jsonpickle import decode
import json
from docker.errors import NotFound

class DockerManagerConnection():

	'''
	Creates a connection with the Docker deamon depending on the parameter dockerUrl. 
	If this value is "None" it means that the Docker deamon should be running in the local host, 
	so in that case the system will use the environment variables to read the configuration 
	and create a connection with Docker deamon. If this parameter is not "None" means that 
	the Docker deamon is running in a remote host and the system should try to connect. 
	It could give errors if the client don't have rights to authenticate or fails the SSL connection.
	'''
	def __init__(self, dockerUrl=None):
		dockerClient = None
		if dockerUrl is None:
			dockerClient = docker.DockerClient(base_url=dockerUrl)
		else:
			dockerClient = docker.from_env()

		if dockerClient is not None and dockerClient.ping():
			containers = dockerClient.containers
			images = dockerClient.images
			self.imageBuilder = ImageBuilder(images, containers)
			self.containerBuilder = ContainerBuilder(containers)


class ImageBuilder():
	def __init__(self, imageDockerObject, containerDockerObject):
		self.imageDockerObject = imageDockerObject
		self.containerDockerObject = containerDockerObject

	'''
	Building process for the image received by parameter.
	'''
	def build(self, image):
		imageObj = decode(image)
		#print(image)
		import os
		#print(imageObj.buildArgs)
		#print(KrakenServer.configuration['config']['imageBase']+":"+imageObj.buildName)
		imageBuilded, buildLogs = self.imageDockerObject.build(	
				path=os.getcwd()+KrakenConfiguration.configuration['config']['pathDockerImages'], 
				dockerfile=KrakenConfiguration.configuration['config']['dockerImages']['BASE'], 
				buildargs=imageObj.buildArgs, 
				tag=imageObj.buildName, 
				shmsize="536870912",
				quiet=False, rm=True, forcerm=True)
		print("Finish to build image...")
		print("Cleaning the dangling images from Docker service")
		self.imageDockerObject.prune(filters={"dangling": True})
		#print(buildLogs)
		#print(type(buildLogs))
		logs = []
		for log in list(buildLogs):
			for dictValue in log.values():
				if str(dictValue) is not None and len(str(dictValue)) > 0:
					logs.append(str(dictValue))


		return json.dumps({	"imageId": imageBuilded.id, 
							"imageLabels": imageBuilded.labels, 
							"imageTags": imageBuilded.tags, 
							"imageLogs": logs })

	'''
	Remove the image specified. In this case will remove the image identified with the tag sent by the user.
	'''
	def delete(self, imageName):
		containersRunning = self.containerDockerObject.list(filters={"ancestor": imageName})
		result = {}
		try:
			for container in containersRunning:
				container.stop()
				container.remove()
		except:
			result["message"] = "Error stopping or removing a running container that uses the specified image"
			return result
		try:
			self.imageDockerObject.remove(image=imageName, force=True, noprune=False)
			result["message"] = "Image deleted from database and docker service."
			return result
		except:
			result["message"] = "Error removing the specified image. Maybe it doesn't exists in the Docker service."
			return result

class ContainerBuilder():
	def __init__(self, containerDockerObject):
		self.containerDockerObject = containerDockerObject
	'''
	print("... Image builded sucessfuly.")
	print("... Creating container: "+namecontainer)
	c = client.containers.run(image, detach = True, name=namecontainer, tty = True,
								environment=["DISPLAY"],
								volumes={'/tmp/.X11-unix/': {'bind': '/tmp/.X11-unix/', 'mode': 'rw'}})
	print("... Container created sucessfuly.")

	'''

	'''
	Create and run the container specified by the user.
	'''
	def create(self, container):
		dockerContainer = self.containerDockerObject.run(
			image=container.buildName,
			auto_remove=container.autoRemove,
			cap_add=container.capAdd,
			cap_drop=container.capDrop,
			detach=True,
			mem_limit=container.memoryLimit,
			name=container.containerName,
			network_mode=container.networkMode,
			ports=container.ports,
			read_only=container.readOnly,
			tty=container.tty,
			volumes=container.volumes,
			privileged=container.privileged, 
			environment=container.environment)
		return dockerContainer

	'''
	Check status for the container name in the parameter. If the container don't exists in Docker service, it returns the message "NOT_FOUND".	
	'''
	def checkStatus(self, containerName):
		try:
			container = self.containerDockerObject.get(containerName)
			if container is not None:
				return container.status
		except NotFound:
			return "NOT_FOUND"
	
	'''
	Stops the specified container searching by name. 
	'''
	def stop(self, containerName):
		container = None
		try:
			container = self.containerDockerObject.get(containerName)
		except NotFound:
			return "NOT_FOUND"
		else:
			if container is not None:
				try:
					container.stop()
					return container.status
				except:
					return "ERROR_STOPPING"
			else:
				return "ERROR_GETTING_CONTAINER"

	'''
	Delete function to remove the container from Docker service. It will try to force the deletion from Docker service.
	'''
	def delete(self, containerName):
		try:
			self.containerDockerObject.remove(containerName, force=True)
			return True
		except:
			return False