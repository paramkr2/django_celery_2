import time

from celery import shared_task
from .generate_data import run

@shared_task
def create_task(task_type):
	print(f'Task Started')
	path = run()
	print(f'Task Ended')
	return path 