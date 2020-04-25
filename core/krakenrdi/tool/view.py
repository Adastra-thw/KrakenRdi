class Tools():
	
	'''
	/tools/stages:
				Methods: GET, POST
				Request: {}
				Description: List of stages for tools.

				Response:
				{"toolStages" : ["common","framework","candc","delivery",
						  				"escalation","exfiltration","exploitation",
						  				"internalrecon","movelateral","recon","weapon","all"]
				} 

	'''
	def stages(self, requestJson):
		pass
	'''


	/tools/list:
				Methods: POST
				Request: {"toolScope" : ["PT","RT"],
						  "toolStage" : ["common","framework","candc","delivery",
						  				"escalation","exfiltration","exploitation",
						  				"internalrecon","movelateral","recon","weapon","all"]
						  }
				Description: List of tools by scope and stage.

				Response:
				{	
					"tools" {
								[
									{
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
									}
								]
					}
				}
	'''
	def list(self, requestJson):
		pass

	'''
	/tools/info:
				Methods: POST
				Request: {"toolName" : "Tool's name"}
				Description: Get basic information about one tool
				Response:
				{
					"toolName": "Tool's name",
					"toolDescription": "Tool's description",
					"toolURL": "Tool's URL",
					"toolScope" ["PT","RT"]
				}
	'''
	def info(self, requestJson):
		pass