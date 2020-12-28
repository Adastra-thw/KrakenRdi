import json
from jsonschema.exceptions import ValidationError
from jsonschema import validate
from core.krakenrdi.api.common.schemas import createBuildSchema, deleteBuildSchema, detailBuildSchema, createContainerSchema, deleteContainerSchema, stopContainerSchema, getContainerSchema, infoToolSchema, filterToolSchema
from core.krakenrdi.api.common.schemas import defaultsBuild, defaultsContainer, defaultsTool              


'''
    Set the default values for the not mandatory attributes in JSON structures.
'''
def __setDefaults(jsonRequest, typeStructure):
    for attribute in typeStructure.keys():
        if attribute not in jsonRequest.keys():
            jsonRequest[attribute] = typeStructure[attribute] 
    return jsonRequest 

def setDefaultsBuild(request):
    structure = __setDefaults(request, defaultsBuild)
    return structure

def setDefaultsContainer(request):
    structure = __setDefaults(request, defaultsContainer)
    return structure

def setDefaultsTool(request):
    structure = __setDefaults(request, defaultsTool)
    return structure

'''
Validation of the JSON structure using the JSON Schema to create builds.
'''
def validateApiRequest(request, abort, schema):
    schemas = {"createBuild": createBuildSchema, 
               "detailBuild": detailBuildSchema, 
               "deleteBuild": deleteBuildSchema, 
               "createContainer": createContainerSchema,
               "deleteContainer": deleteContainerSchema,
               "stopContainer": stopContainerSchema,
               "getContainer": getContainerSchema, 
               "infoToolSchema": infoToolSchema,
               "filterToolSchema": filterToolSchema
               }
    if request.is_json is False:
        abort(400)
    if schema not in schemas.keys():
        abort(400)
    try:
        validate(instance=request.json, schema=schemas[schema])
    except ValidationError as err:
        print(err._word_for_schema_in_error_message)
        abort(400, err.message)
    return True

class BusinessValidations:
    def __init__(self, dockerManager):
        self.dockerManager = dockerManager

    def validateBuildStructure(self):
        pass

    def validateContainerStructure(self, container):
        containerStructure = {}
        containerStructure["valid"] = False
        #Validate build name. Check if the image exists in Docker service.
        try:
            self.dockerManager.imageBuilder.imageDockerObject.get(container["buildName"]) 
        except:
            containerStructure["message"] = "Image don't found"
            return containerStructure

        containerStructure["buildName"]=container["buildName"]
        #Validate container name. Check if the container name is already Docker service.
        if "containerName" in container:
            containerStructure["containerName"]=container["containerName"]
            containerFound=None
            try:
                containerFound = self.dockerManager.containerBuilder.containerDockerObject.get(container["containerName"]) 
            except:
                #If the container is not found means that it could be created without problem.
                #If there's no exception means the container already has beed created and should not continue with this process.
                pass

            if "removeIfExists" in container and containerFound is not None:
                containerFound.stop(timeout=30)
                containerFound.remove()
            elif containerFound is not None:
                containerStructure["message"] = "Container "+container["containerName"]+" already exists. Choose another name or set the flag 'removeIfExists' to delete the container with that name and create yours."
                return containerStructure

        containerStructure["volumes"] = {}
        containerStructure["ports"] = {}
        containerStructure["environment"] = []

        #Validate and create the appropiate structure.
        if "ports" in container:
            portStructure={}
            for port in container["ports"]:
                #The keys will be the ports inside container.
                #The values will be the ports in the host machine.
                portContainer = None
                portHost = None

                if "portContainer" in port:
                    if "protocolContainer" not in port:
                        port["protocolContainer"] = "/tcp"
                    else:
                        port["protocolContainer"] = "/"+port["protocolContainer"]
                    portContainer = str(port["portContainer"])+port["protocolContainer"]

                if "portHost" in port:                    
                    if "protocolHost" not in port:
                        port["protocolHost"] = "/tcp"
                    else:
                        port["protocolHost"] = "/"+port["protocolHost"]
                    portHost = str(port["portHost"])+port["protocolHost"]

                #This could be, for example:
                #{"22/tcp": None} -- 22/tcp in container / Random in host.
                #{"22/tcp": "2222/tcp"}  -- 22/tcp in container / 2222/tcp in host.
                portStructure[portContainer] = portHost
            containerStructure["ports"]=portStructure

        if "volumes" in container:
            #The keys will be the volume in the host machine.
            #The values will be mount point inside the container.                
            volumes={}
            for volume in container["volumes"]:
                hostVolume = volume["hostVolume"]
                containerVolume = {"bind": volume["containerVolume"], 
                                    "mode": volume["modeVolume"]}
                volumes[hostVolume] = containerVolume
            
            #This could be, for example:
            #{ '/home/user1/': {'bind': '/mnt/vol2', 'mode': 'rw'}, 
            #  '/var/www': {'bind': '/mnt/vol1', 'mode': 'ro'}}
            containerStructure["volumes"]=volumes

        #Validate the value of memory
        import re
        if "memoryLimit" in container:
            match = re.compile('(\d*)(?:b|k|m|g|)').match(container["memoryLimit"])
            if match:
                containerStructure["memoryLimit"]=container["memoryLimit"]
            else:
                containerStructure["message"] =  "Invalid memory limit: "+container["memoryLimit"]+". Valid examples could be: 100000b, 1000k, 128m, 1g, etc."

        #Verify if X11 should be enabled.
        if "enableX11" in container:
            from os import environ
            containerStructure["environment"].extend(["DISPLAY="+environ["DISPLAY"]]),
            containerStructure["volumes"].update({'/tmp/.X11-unix/': {'bind': '/tmp/.X11-unix/', 'mode': 'rw'}})
        #No special validations.
        containerStructure["autoRemove"]= container["autoRemove"]
        containerStructure["capAdd"]= container["capAdd"]
        containerStructure["capDrop"]= container["capDrop"]
        containerStructure["hostname"]=container["hostname"]
        
        containerStructure["networkMode"]=container["networkMode"]
        containerStructure["privileged"]=container["privileged"]
        containerStructure["networkDisabled"]=container["networkDisabled"]
        containerStructure["readOnly"]=container["readOnly"]
        containerStructure["removeOnFinish"]=container["removeOnFinish"]
        containerStructure["valid"] = True
        return containerStructure