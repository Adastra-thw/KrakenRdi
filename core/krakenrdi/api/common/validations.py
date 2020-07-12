import json
from jsonschema.exceptions import ValidationError
from jsonschema import validate
from core.krakenrdi.api.common.schemas import createBuildSchema, deleteBuildSchema, detailBuildSchema, createContainerSchema, infoToolSchema, filterToolSchema
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