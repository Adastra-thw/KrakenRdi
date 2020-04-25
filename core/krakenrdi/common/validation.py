import json
import jsonschema
from jsonschema import validate

# Describe what kind of json you expect.
studentSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "rollnumber": {"type": "number"},
        "marks": {"type": "number"},
    },
}

def validateJson(jsonData):
    try:
        validate(instance=jsonData, schema=studentSchema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True

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

