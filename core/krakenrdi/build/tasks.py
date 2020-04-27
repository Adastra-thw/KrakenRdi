from __future__ import absolute_import

import time
from celery import Celery, task

'''
	Create a new build. If the docker build have success a new image will be generated. 
'''
@task()
def createBuild(buildJson):
	print(buildJson)
	return buildJson
'''
	Duplicate an existing build
'''
@task()
def duplicateBuild(buildJson):
	print(222)