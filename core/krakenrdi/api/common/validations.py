import json
import jsonschema
from jsonschema import validate

'''
JSON Schema used to create a building. 
'''
createBuildSchema = {
    "type": "object",
    "properties": {
        "buildName": {  "type": "string",  
                        "maxLength": 20, 
                        "minLength": 2},
        "buildScope": { "type": "array", 
                        "minItems": 1, 
                        "items": {"enum": ["common", "frameworks", "anon", "recon", 
                                           "weaponization", "delivery", "exploitation", 
                                           "persistence", "commandcontrol", "internalrecon", 
                                           "movelaterally", "exfiltration"] }},
        "tools": {"type": "array", 
                  "minItems": 1,
                  "items": {"enum": ["THC_HYDRA", "CeWL", "Postman", "FuzzDB", 
                                    "DirBuster", "MetasploitFramework", "BeEF", 
                                    "Bettercap", "TOR - From Debian repository", 
                                    "TOR - From source code.", "TORSocks", "ProxyChains-ng", 
                                    "Recon-NG", "Photon", "theHarvester", 
                                    "SkipTracer", "Metagoofil", "JustMetadata", "SpiderFoot", 
                                    "Maltego", "Nmap", "CVE2018_20250", "CVE2017_8759", "CVE2017_8570", 
                                    "CVE2017_0199", "DEMIGUISE", "MALICIOUSMACROGENERATOR", 
                                    "OFFICEDDEPAYLOADS", "DONTKILLMYCAT(DKMC)", 
                                    "EMBEDINHTML", "MACRO_PACK"] }},
        "containerProperties": {"type": "object", 
                                "required": ["USERNAME","PASSWORD"],
                                "properties": {
                                    "USERNAME": {"type": "string", 
                                                 "maxLength": 20},
                                    "PASSWORD": {"type": "string", 
                                                 "maxLength": 20},
                                    "EXPOSE_PORTS": {"type": "array", 
                                                     "minItems": 1,
                                                     "uniqueItems": True,
                                                     "items": {
                                                     "type": "number"}},
                                    "RUBY_VERSION": {"type": "string", 
                                                 "maxLength": 10},
                                    "RVM_DIR": {"type": "string", 
                                                 "maxLength": 40},
                                    "RVM_LOADER": {"type": "string", 
                                                 "maxLength": 40},   
                                    "POSTGRES_PASSWORD": {"type": "string", 
                                                 "maxLength": 20},
                                    "POSTGRES_DB_NAME": {"type": "string", 
                                                 "maxLength": 20},
                                    "POSTGRES_DB_USERNAME": {"type": "string", 
                                                 "maxLength": 20},
                                    "POSTGRES_DB_PASSWORD": {"type": "string", 
                                                 "maxLength": 20},


                                },
                                "additionalProperties": False},
        "startSSH": {"type": "boolean"},
        "startPostgres": {"type": "boolean"},
        "additionalProperties": False,
    },
    "required": ["buildName", "buildScope", "tools"]
}

'''
Validation of the JSON structure using the JSON Schema to create builds.
'''
def validateCreateBuild(request, abort):
    if request.is_json is False:
        abort(400)
    try:
        validate(instance=request.json, schema=createBuildSchema)
    except jsonschema.exceptions.ValidationError as err:
        #print(err._word_for_schema_in_error_message)
        abort(400, err.message)
    return True
'''
# Convert json to python object.
jsonData = json.loads('{"name": "jane doe", "rollnumber": "25", "marks": 72}')
# validate it
isValid = validateJson(jsonData)
if isValid:
    print(jsonData)
    print("Given JSON data is Valid")
else:
    print(jsonData)
    print("Given JSON data is InValid")

# Convert json to python object.
jsonData = json.loads('{"name": "jane doe", "rollnumber": 25, "marks": 72}')
# validate it
isValid = validateJson(jsonData)
if isValid:
    print(jsonData)
    print("Given JSON data is Valid")
else:
    print(jsonData)
    print("Given JSON data is InValid")

'''