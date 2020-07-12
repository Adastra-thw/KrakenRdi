from core.krakenrdi.server.CoreObjects import KrakenConfiguration
import docker 
from jsonpickle import decode
import json

class DockerManagerConnection():

	'''
	Creates a connection with the Docker deamon depending on the parameter dockerUrl. 
	If this value is "None" it means that the Docker deamon should be running in the local host, 
	son in that case the system will use the environment variables to read the configuration 
	to create a connection with Docker deamon. If this parameter is not "None" means that 
	the Docker deamon is running in a remote host and the system should try to connect.   
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
			self.imageBuilder = ImageBuilder(images)
			self.containerBuilder = ContainerBuilder(containers)


class ImageBuilder():
	def __init__(self, imageDockerObject):
		self.imageDockerObject = imageDockerObject

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
		return json.dumps({	"imageId": imageBuilded.id, 
							"imageLabels": imageBuilded.labels, 
							"imageTags": imageBuilded.tags})

	'''
	Remove the image specified. In this case will remove the image identified with the tag sent by the user.
	'''
	def delete(self, image):
		self.imageBuilder.delete(image)


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
		dockerContainer = self.containerDockerObject.create(
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
			volumes=container.volumes
		)
		print(dockerContainer.status)


	def checkStatus(self, container):
		self.containerDockerObject.inspect(container)

	def stop(self, container):
		pass

	def destroy(self, container):
		pass
