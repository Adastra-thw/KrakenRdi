class BuildController():

	'''
	/build/list:
				Methods: GET, POST
				Request: {}
				Description: List every build created.

				Response:
				{
					builds: [
								{
									"buildName":"Build Name", 
									"buildDescription":"Build Description",
									"buildDate":"Build Date",
									"buildTools":"Number of tools",
									"buildContainers":"Build Containers",
								}, 
								{
									"buildName":"Build Name", 
									"buildDescription":"Build Description",
									"buildDate":"Build Date",
									"buildTools":"Number of tools",
									"buildContainers":"Build Containers",
								}
						]
					}
	'''
	def list(self, requestJson):
		pass

	'''
	/build/details:
				Methods: POST
				Request;
					{
						"buildName": "Name for the build"
					}
				Description: Detailed information for the build.

				Response:
				{	
					"buildStages": ["common","framework","candc","delivery",
		  							"escalation","exfiltration","exploitation",
		  							"internalrecon","movelateral","recon","weapon","all"],
		  			"buildTools" : [{
										"toolName": "Tool's name",
										"toolDescription": "Tool's description",
										"toolURL": "Tool's URL",
										"toolScope" ["PT","RT"]
									}, 
									{	
										"toolName": "Tool's name2",
										"toolDescription": "Tool's description2",
										"toolURL": "Tool's URL2",
										"toolScope" ["PT","RT"]
									}]
				}, 
	'''
	def details(self, requestJson):
		pass

	'''
	/build/duplicate:
				Methods: POST
				Request:
					{
						"buildName": "Name for the build to search",
						"buildNameDuplicated": "Name for the duplicated build"
					}
				Description: Duplicate an existing build.

				Response:
				{
					"message" : "OK"
				}
	'''
	def duplicate(self, requestJson):
		pass

	'''
	/build/delete:
				Methods: POST
				Request:
					{
						"buildName": "Name for the build to search"
					}
				Description: Delete an existing build.

				Response:
				{
					"message" : "OK"
				}
	'''
	def delete(self, requestJson):
		pass

	'''
	/build/filter:
				Methods: POST
				Request: {}
				Description: List every build created.
				Response:
				{
					"buildName":"Build Name", 
					"buildDescription":"Build Description",
					"buildDate":"Build Date",
					"buildTools":"Number of tools",
					"buildContainers":"Build Containers",
				}
	'''
	def filter(self, requestJson):
		pass

	'''
	/build/create:
				Methods: POST, PUT
				Request: {
							"buildName" : "Build Name. Will be the Docker image tag",
							"buildScpe" : {"anon","recon","weapon","framework", "etc..."},
							"tools" : ["PROPERTY_ENABLED_FOR_TOOL1","PROPERTY_ENABLED_FOR_TOOL2","PROPERTY_ENABLED_FOR_TOOL3"]
							"containerProperties" : {
								"USERNAME" : "Value", 
								"PASSWORD" : "Value",
								"OtherProp" : "Value"
	 						}
	 						"startSSH" : true/false
	 						"startPostgres": true/false
	 						"exposedPorts": "22 110 2222 8080 8181"
						}
				Description: Create a new build and let it running in background (docker build command).
				Response:
				{
					"message" : "Request for build creation received."			
				}
	'''
	def create(self, requestJson):
		pass

	'''
	/build/status:
				Methods: POST, PUT
				Request: {
							"buildName" : "Build Name. Will be the Docker image tag"
						}
				Description: Show the status of the build.
				Response:
				{
					"message" : "REQUESTED|RUNNING|FINISHED|ERROR"			
				}
	'''
	def status(self, requestJson):
		pass