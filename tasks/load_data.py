
import csv
from createmodels.models import StoreStatus,BusinessHours,StoreTimezone
from itertools import islice
from collections import defaultdict
from datetime import datetime, timezone


def get_row_store_status(reader):
	lis = []
	for row in reader :
		x = StoreStatus(storeid=row[0], status=row[1] , date_utc=row[2][:10] , time_utc=row[2][11:-5])   
		lis.append( x )
	return lis

def get_row_business_hours(reader):
	lis = []
	for row in reader :
		x = BusinessHours(storeid=row[0],dayofweek=row[1], start_time=row[2] , end_time=row[3])   
		lis.append( x )
	return lis

def get_row_store_timezone(reader):
	lis = []
	for row in reader :
		x = StoreTimezone(storeid=row[0],timezone=row[1])   
		lis.append( x )
	return lis

def load():
	global StoreStatus
	lis = []
	StoreStatus.objects.all().delete()
	BusinessHours.objects.all().delete()
	StoreTimezone.objects.all().delete()
	files = ['store_status','business_hours', 'store_timezone']
	for filename in files:
		with open(f'files/{filename}.csv') as file:
			reader = csv.reader(file)
			next(reader)  # Advance past the header
			reader = reader
		
			if filename =='store_status': 
				lis = get_row_store_status(reader)
				obj = StoreStatus
			elif filename=='business_hours': 
				lis = get_row_business_hours(reader)
				obj = BusinessHours
			else: 
				lis = get_row_store_timezone(reader)
				obj = StoreTimezone	
			print(f' Filename:{filename} Total enties:{len(lis)}  ' )
			
			i = 0			
			while i<100:
				batch = lis[i*50000:(i+1)*50000]
				if len(batch)==0: 
					break 
				obj.objects.bulk_create(batch,batch_size=50000, ignore_conflicts=True,update_conflicts=False)
				print(f'Inserted:{i*50000}')
				i+=1
	
			
	return 'loaded'	