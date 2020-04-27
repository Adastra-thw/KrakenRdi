import time
from celery import Celery, task

@task()
def createContainer(self, containerJson):
	print(containerJson)
	time.sleep(4)