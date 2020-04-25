import json
import os,sys
import jsonschema

from core.krakenrdi.build.controller import BuildController
from core.krakenrdi.build.view import BuildView
from core.krakenrdi.server import Server

class KrakenRDI():
	
	def startup(self):
		self.configuration = {}
		self.tools = {}
		self.arguments = {}
		try:
			with open('config/config.json') as configFile:
				self.configuration = json.load(configFile)
		except:
			print("Failed reading configuration from <KRAKENRID_DIR>/config/config.json")
			sys.exit(1)

		try:
			with open('config/tools.json') as toolsFile:
				self.tools = json.load(toolsFile)
		except:
			print("Failed reading configuration from <KRAKENRID_DIR>/config/tools.json")
			sys.exit(1)

		try:
			with open('config/arguments.json') as argumentsFile:
				self.arguments = json.load(argumentsFile)
		except:
			print("Failed reading configuration from <KRAKENRID_DIR>/config/arguments.json")
			sys.exit(1)
		Server.init(self.configuration, self.tools, self.arguments)
		Server.startServer()

if __name__ == '__main__':
	kraken = KrakenRDI()
	kraken.startup()