class Image():
	def __init__(self):
		self.buildName=None
		self.buildArgs={}
		self.buildScope=None
		self.memoryLimit=None
		self.extraHostIP=None #--add-host=docker:10.180.0.1
		self.startSSH=False
		self.startPostgres=False

class Container():
	def __init__(self):
		self.buildName=None
		self.containerName=None
		self.autoRemove=False
		self.capAdd=["ALL"]
		self.capDrop=[""]
		self.hostname=None
		self.memoryLimit=None
		self.networkMode= "host"
		self.networkDisabled=False
		self.readOnly=False
		self.ports={}
		self.volumes=[]
		self.tty=True
		self.privileged=False
		self.startSSH = False
		self.startPostgres = False


class Tool():
	def __init__(self):
		self.buildName=None
		self.buildTag=None
		self.buildDate=None
		self.buildScope=None