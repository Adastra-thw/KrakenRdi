import docker

client = docker.from_env()

image = "adastra/docker-for-redteam"
namecontainer="reddocker"
options = { "VERSION":"latest", 
			"RECON_RECONNG":"True"}

#Stop all containers first.
print("... List and stop all containers.")
#for container in client.containers.list():
#	container.stop()
print("... Prune all containers.")		
#client.containers.prune()
#client.images.prune()
#client.volumes.prune()

print("... Building image.")
client.images.build(path="./config/docker", 
					dockerfile="Dockerfile-base", 
					buildargs=options, 
					tag="adastra/docker-for-redteam:latest", 
					shmsize="536870912",
					quiet=False, rm=True)
print("... Image builded sucessfuly.")
print("... Creating container: "+namecontainer)
c = client.containers.run(image, detach = True, name=namecontainer, tty = True,
							environment=["DISPLAY"],
							volumes={'/tmp/.X11-unix/': {'bind': '/tmp/.X11-unix/', 'mode': 'rw'}})
print("... Container created sucessfuly.")
'''
c = client.containers.run(image, detach = True, tty = True)
print "[+] New container created: {0} ({1})".format(c.short_id, c.name)
'''