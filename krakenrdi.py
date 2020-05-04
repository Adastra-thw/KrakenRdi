import json
import os,sys
from plumbum import cli
from core.krakenrdi.server.CoreObjects import KrakenConfiguration
from core.krakenrdi.server.krakenServer import KrakenServer
from core.krakenrdi.api.build.view import BuildView
from core.krakenrdi.api.container.view import ContainerView

class KrakenRDI(cli.Application):
	restApiCli = cli.Flag(["-r", "--start-restapi"], help = "Start Rest API.")
	workerCli = cli.Flag(["-w" , "--start-worker"], help = "Start Celery worker.")

	def main(self):
		if self.restApiCli or self.workerCli:
			print("Initialization tasks...")
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
			KrakenServer.init(self.configuration, self.tools, self.arguments)
			print("Configuration established.")
			KrakenServer.configureServices()
			print("Core services for the Rest API configured.")
			


		if self.restApiCli:
			print("Starting webserver and Rest API...")
			self.startRestApi()
		elif self.workerCli:
			print("Starting Celery worker...")
			self.startWorker()

	def startRestApi(self):
		KrakenConfiguration.restApi.run()

	def startWorker(self):
		from celery import Celery, task
		from celery import current_app
		from celery.bin import worker

		
		application = current_app._get_current_object()
		worker = worker.worker(app=application)
		options = {
			'broker': KrakenConfiguration.restApi.config['CELERY_BROKER_URL'],
			'loglevel': 'INFO',
			'traceback': True,
		}
		worker.run(**options)
		#print("Worker started successfully. Now, from other terminal start the Rest Api to complete the Kraken startup...")

		


if __name__ == '__main__':
	KrakenRDI.run()